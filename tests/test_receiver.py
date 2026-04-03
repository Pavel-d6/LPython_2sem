
import pytest
from task import Task
from receiver import TaskReceiver
from src.generator_source import GeneratorTaskSource


def make_task(id: str = "t-1") -> Task:
    return Task(id=id, description="тест", priority=5, payload="data")


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
        assert TaskReceiver().source_count == 0

    def test_register_valid_source(self) -> None:
        r = TaskReceiver()
        r.register(DummySource([]))
        assert r.source_count == 1

    def test_register_invalid_source_raises(self) -> None:
        with pytest.raises(TypeError, match="не реализует протокол TaskSource"):
            TaskReceiver().register(NotASource())

    def test_collect_all_from_single_source(self) -> None:
        tasks = [make_task()]
        r = TaskReceiver()
        r.register(DummySource(tasks))
        assert r.collect_all() == tasks

    def test_collect_all_from_multiple_sources(self) -> None:
        r = TaskReceiver()
        r.register(DummySource([make_task("a1"), make_task("a2")]))
        r.register(DummySource([make_task("b1")]))
        assert len(r.collect_all()) == 3

    def test_collect_all_empty_sources(self) -> None:
        r = TaskReceiver()
        r.register(DummySource([]))
        assert r.collect_all() == []

    def test_collect_from_valid_source(self) -> None:
        tasks = TaskReceiver().collect_from(GeneratorTaskSource(count=3))
        assert len(tasks) == 3

    def test_collect_from_invalid_source_raises(self) -> None:
        with pytest.raises(TypeError):
            TaskReceiver().collect_from(NotASource())

    def test_register_multiple_sources(self) -> None:
        r = TaskReceiver()
        r.register(GeneratorTaskSource(count=2))
        r.register(GeneratorTaskSource(count=3))
        assert r.source_count == 2

    def test_collect_all_order_preserved(self) -> None:
        r = TaskReceiver()
        r.register(DummySource([make_task("first")]))
        r.register(DummySource([make_task("second")]))
        result = r.collect_all()
        assert result[0].id == "first"
        assert result[1].id == "second"