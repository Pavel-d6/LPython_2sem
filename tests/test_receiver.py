import pytest

from receiver import TaskReceiver
from task import Task
from src.generator_source import GeneratorTaskSource


class DummySource:
    def __init__(self, tasks: list[Task]) -> None:
        self._tasks = tasks

    def get_tasks(self) -> list[Task]:
        return self._tasks


class NotASource:
    def fetch_data(self) -> list[Task]:
        return []


class TestTaskReceiver:
    def test_initial_source_count_is_zero(self) -> None:
        receiver = TaskReceiver()
        assert receiver.source_count == 0

    def test_register_valid_source(self) -> None:
        receiver = TaskReceiver()
        receiver.register(DummySource([]))
        assert receiver.source_count == 1

    def test_register_invalid_source_raises(self) -> None:
        receiver = TaskReceiver()
        with pytest.raises(TypeError, match="не реализует протокол TaskSource"):
            receiver.register(NotASource())

    def test_collect_all_from_single_source(self) -> None:
        tasks = [Task(id="t1", payload="data")]
        receiver = TaskReceiver()
        receiver.register(DummySource(tasks))
        assert receiver.collect_all() == tasks

    def test_collect_all_from_multiple_sources(self) -> None:
        source_a = DummySource([Task(id="a1", payload="x"), Task(id="a2", payload="y")])
        source_b = DummySource([Task(id="b1", payload="z")])
        receiver = TaskReceiver()
        receiver.register(source_a)
        receiver.register(source_b)
        result = receiver.collect_all()
        assert len(result) == 3

    def test_collect_all_empty_sources(self) -> None:
        receiver = TaskReceiver()
        receiver.register(DummySource([]))
        assert receiver.collect_all() == []

    def test_collect_from_valid_source(self) -> None:
        source = GeneratorTaskSource(count=3)
        receiver = TaskReceiver()
        tasks = receiver.collect_from(source)
        assert len(tasks) == 3

    def test_collect_from_invalid_source_raises(self) -> None:
        receiver = TaskReceiver()
        with pytest.raises(TypeError):
            receiver.collect_from(NotASource())

    def test_register_multiple_sources(self) -> None:
        receiver = TaskReceiver()
        receiver.register(GeneratorTaskSource(count=2))
        receiver.register(GeneratorTaskSource(count=3))
        assert receiver.source_count == 2

    def test_collect_all_order_preserved(self) -> None:
        t1 = Task(id="first", payload="a")
        t2 = Task(id="second", payload="b")
        receiver = TaskReceiver()
        receiver.register(DummySource([t1]))
        receiver.register(DummySource([t2]))
        result = receiver.collect_all()
        assert result[0].id == "first"
        assert result[1].id == "second"
