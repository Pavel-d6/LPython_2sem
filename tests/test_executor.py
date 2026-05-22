import asyncio
import json
import pytest

from task import Task, Status
from executor import TaskExecutor
from handlers.registry import HandlerRegistry
from src.generator_source import GeneratorTaskSource
from src.sourse_from_file import FileTaskSource
from src.flask_source import FlaskApiTaskSource
from receiver import TaskReceiver


class InstantHandler:
    """Выполняет задачу мгновенно."""
    async def handle(self, task: Task) -> None:
        pass


class FailingHandler:
    """Всегда бросает исключение."""
    async def handle(self, task: Task) -> None:
        raise RuntimeError("сбой обработчика")


class TrackingHandler:
    """Записывает порядок обработки."""
    def __init__(self):
        self.handled: list[str] = []

    async def handle(self, task: Task) -> None:
        self.handled.append(task.id)


def make_queue(tasks: list[Task]) -> asyncio.Queue:
    q: asyncio.Queue = asyncio.Queue()
    for t in tasks:
        q.put_nowait(t)
    return q


def make_registry(handler=None) -> HandlerRegistry:
    registry = HandlerRegistry()
    registry.register("default", handler or InstantHandler())
    return registry


def make_task(task_id: str = "t-1", priority: int = 5) -> Task:
    return Task(id=task_id, description="тест", priority=priority, payload="data")


@pytest.mark.asyncio
async def test_task_reaches_done_status():
    task = make_task()
    queue = make_queue([task])
    async with TaskExecutor(queue, make_registry()):
        pass
    assert task.status == Status.DONE


@pytest.mark.asyncio
async def test_all_tasks_processed():
    tasks = [make_task(f"t-{i}") for i in range(6)]
    queue = make_queue(tasks)
    async with TaskExecutor(queue, make_registry(), workers=3):
        pass
    assert all(t.status == Status.DONE for t in tasks)


@pytest.mark.asyncio
async def test_queue_is_empty_after_processing():
    tasks = [make_task(f"t-{i}") for i in range(4)]
    queue = make_queue(tasks)
    async with TaskExecutor(queue, make_registry()):
        pass
    assert queue.empty()


@pytest.mark.asyncio
async def test_failing_handler_does_not_kill_worker():
    bad = make_task("bad")
    good = make_task("good")
    queue = make_queue([bad, good])
    async with TaskExecutor(queue, make_registry(FailingHandler()), workers=2):
        pass
    assert bad.status == Status.IN_PROGRESS   # complete() не вызван — ожидаемо
    assert good.status == Status.IN_PROGRESS


@pytest.mark.asyncio
async def test_error_in_one_task_does_not_block_others():
    tasks = [make_task(f"t-{i}") for i in range(5)]
    bad = make_task("bad")
    all_tasks = tasks + [bad]

    registry = HandlerRegistry()
    registry.register("default", InstantHandler())
    registry.register("broken", FailingHandler())

    broken_task = Task(id="broken-1", description="сломана", priority=3,
                       payload="x", task_type="broken")
    queue = make_queue([broken_task] + tasks)
    async with TaskExecutor(queue, registry, workers=3):
        pass
    assert all(t.status == Status.DONE for t in tasks)


# ---------------------------------------------------------------------------
# Контекстный менеджер и ручной старт/стоп
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_context_manager_completes_all_tasks():
    tasks = [make_task(f"t-{i}") for i in range(3)]
    queue = make_queue(tasks)
    async with TaskExecutor(queue, make_registry(), workers=2):
        pass
    assert all(t.status == Status.DONE for t in tasks)


@pytest.mark.asyncio
async def test_manual_start_stop():
    tasks = [make_task(f"t-{i}") for i in range(3)]
    queue = make_queue(tasks)
    executor = TaskExecutor(queue, make_registry(), workers=2)
    await executor.start()
    await executor.stop()
    assert all(t.status == Status.DONE for t in tasks)


@pytest.mark.asyncio
async def test_workers_count_creates_correct_number_of_tasks():
    queue: asyncio.Queue = asyncio.Queue()
    executor = TaskExecutor(queue, make_registry(), workers=5)
    await executor.start()
    assert len(executor._tasks) == 5
    await executor.stop()



@pytest.mark.asyncio
async def test_with_generator_source():
    source = GeneratorTaskSource(count=5)
    tasks = source.get_tasks()
    queue = make_queue(tasks)
    async with TaskExecutor(queue, make_registry()):
        pass
    assert all(t.status == Status.DONE for t in tasks)


@pytest.mark.asyncio
async def test_with_generator_source_custom_factory():
    factory = lambda i: Task(id=f"order-{i}", description=f"заказ {i}",
                             priority=(i % 10) + 1, payload={"order_id": i})
    tasks = GeneratorTaskSource(count=4, factory=factory).get_tasks()
    queue = make_queue(tasks)
    async with TaskExecutor(queue, make_registry()):
        pass
    assert all(t.status == Status.DONE for t in tasks)


@pytest.mark.asyncio
async def test_with_file_source(tmp_path):
    data = [
        {"id": "f-1", "description": "задача 1", "priority": 5, "payload": "x"},
        {"id": "f-2", "description": "задача 2", "priority": 3, "payload": "y"},
    ]
    f = tmp_path / "tasks.json"
    f.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    tasks = FileTaskSource(f).get_tasks()
    queue = make_queue(tasks)
    async with TaskExecutor(queue, make_registry()):
        pass
    assert all(t.status == Status.DONE for t in tasks)


@pytest.mark.asyncio
async def test_with_receiver_collect_all(tmp_path):
    data = [{"id": "f-1", "description": "из файла", "priority": 4, "payload": "z"}]
    f = tmp_path / "tasks.json"
    f.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    receiver = TaskReceiver()
    receiver.register(GeneratorTaskSource(count=3))
    receiver.register(FileTaskSource(f))
    tasks = receiver.collect_all()

    queue = make_queue(tasks)
    async with TaskExecutor(queue, make_registry()):
        pass
    assert len(tasks) == 4
    assert all(t.status == Status.DONE for t in tasks)


@pytest.mark.asyncio
async def test_with_flask_source_unavailable():
    """FlaskApiTaskSource при недоступном сервере бросает ConnectionError."""
    source = FlaskApiTaskSource("http://localhost:19999")
    with pytest.raises(ConnectionError):
        source.get_tasks()
