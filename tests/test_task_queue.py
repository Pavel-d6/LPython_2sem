import types
import pytest
from task import Task, Status
from Task_queue import TaskQueue


def make_task(id: str, priority: int = 5, status: Status = Status.PENDING) -> Task:
    t = Task(id=id, description=f"задача {id}", priority=priority, payload=f"data-{id}")
    if status == Status.IN_PROGRESS:
        t.start()
    elif status == Status.DONE:
        t.start()
        t.complete()
    return t


class TestTaskQueueBasic:
    def test_empty_queue_length(self) -> None:
        assert len(TaskQueue()) == 0

    def test_init_with_tasks(self) -> None:
        tasks = [make_task("t1"), make_task("t2")]
        q = TaskQueue(tasks)
        assert len(q) == 2
        assert list(q) == tasks

    def test_add_increases_length(self) -> None:
        q = TaskQueue()
        q.add(make_task("t1"))
        assert len(q) == 1

    def test_add_non_task_raises(self) -> None:
        with pytest.raises(TypeError):
            TaskQueue().add("not a task")  # type: ignore[arg-type]

    def test_contains(self) -> None:
        q = TaskQueue()
        t = make_task("t1")
        q.add(t)
        assert t in q

    def test_not_contains(self) -> None:
        assert make_task("t1") not in TaskQueue()


class TestTaskQueueIteration:
    def test_iterate_empty_queue(self) -> None:
        assert list(TaskQueue()) == []

    def test_iterate_returns_all_tasks(self) -> None:
        q = TaskQueue()
        tasks = [make_task("t1"), make_task("t2"), make_task("t3")]
        for t in tasks:
            q.add(t)
        assert list(q) == tasks

    def test_order_preserved(self) -> None:
        q = TaskQueue()
        q.add(make_task("first"))
        q.add(make_task("second"))
        result = list(q)
        assert result[0].id == "first"
        assert result[1].id == "second"

    def test_repeated_iteration(self) -> None:
        q = TaskQueue()
        q.add(make_task("t1"))
        q.add(make_task("t2"))
        assert list(q) == list(q)

    def test_iter_returns_generator(self) -> None:
        assert isinstance(iter(TaskQueue()), types.GeneratorType)

    def test_compatible_with_sum(self) -> None:
        q = TaskQueue()
        q.add(make_task("t1", priority=3))
        q.add(make_task("t2", priority=7))
        assert sum(t.priority for t in q) == 10

    def test_compatible_with_list(self) -> None:
        q = TaskQueue()
        q.add(make_task("t1"))
        assert isinstance(list(q), list)

    def test_stop_iteration_on_empty(self) -> None:
        with pytest.raises(StopIteration):
            next(iter(TaskQueue()))


class TestTaskQueueFilters:
    def setup_method(self) -> None:
        self.queue = TaskQueue()
        self.queue.add(make_task("p1", priority=2, status=Status.PENDING))
        self.queue.add(make_task("p2", priority=5, status=Status.PENDING))
        self.queue.add(make_task("i1", priority=7, status=Status.IN_PROGRESS))
        self.queue.add(make_task("d1", priority=9, status=Status.DONE))

    def test_filter_by_status_pending(self) -> None:
        result = list(self.queue.filter_by_status(Status.PENDING))
        assert len(result) == 2
        assert all(t.status == Status.PENDING for t in result)

    def test_filter_by_status_in_progress(self) -> None:
        result = list(self.queue.filter_by_status(Status.IN_PROGRESS))
        assert len(result) == 1
        assert result[0].id == "i1"

    def test_filter_by_status_done(self) -> None:
        result = list(self.queue.filter_by_status(Status.DONE))
        assert len(result) == 1
        assert result[0].id == "d1"

    def test_filter_by_priority_min(self) -> None:
        result = list(self.queue.filter_by_priority(min_priority=7))
        assert all(t.priority >= 7 for t in result)

    def test_filter_by_priority_range(self) -> None:
        result = list(self.queue.filter_by_priority(min_priority=5, max_priority=7))
        assert len(result) == 2

    def test_filters_are_lazy(self) -> None:
        gen = self.queue.filter_by_status(Status.PENDING)
        assert isinstance(gen, types.GeneratorType)

    def test_filter_by_priority_is_lazy(self) -> None:
        gen = self.queue.filter_by_priority(min_priority=5)
        assert isinstance(gen, types.GeneratorType)

    def test_empty_filter_result(self) -> None:
        result = list(self.queue.filter_by_status(Status.PENDING))
        q = TaskQueue()
        q.add(make_task("d1", status=Status.DONE))
        assert list(q.filter_by_status(Status.PENDING)) == []
