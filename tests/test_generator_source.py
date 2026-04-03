
import pytest
from task import Task
from protocol import TaskSource
from src.generator_source import GeneratorTaskSource


class TestGeneratorTaskSource:
    def test_generates_correct_count(self) -> None:
        assert len(GeneratorTaskSource(count=5).get_tasks()) == 5

    def test_default_factory_produces_valid_tasks(self) -> None:
        for task in GeneratorTaskSource(count=3).get_tasks():
            assert isinstance(task, Task)
            assert task.id
            assert task.description
            assert task.payload

    def test_default_ids_are_unique(self) -> None:
        ids = [t.id for t in GeneratorTaskSource(count=10).get_tasks()]
        assert len(set(ids)) == len(ids)

    def test_default_priority_in_range(self) -> None:
        for task in GeneratorTaskSource(count=10).get_tasks():
            assert 1 <= task.priority <= 10

    def test_custom_factory_is_used(self) -> None:
        factory = lambda i: Task(id=f"custom-{i}", description="тест", priority=3, payload=f"job-{i}")
        tasks = GeneratorTaskSource(count=3, factory=factory).get_tasks()
        assert tasks[0].id == "custom-0"
        assert tasks[1].id == "custom-1"
        assert tasks[2].id == "custom-2"

    def test_zero_count_raises(self) -> None:
        with pytest.raises(ValueError, match="положительным"):
            GeneratorTaskSource(count=0)

    def test_negative_count_raises(self) -> None:
        with pytest.raises(ValueError):
            GeneratorTaskSource(count=-5)

    def test_satisfies_task_source_protocol(self) -> None:
        assert isinstance(GeneratorTaskSource(count=1), TaskSource)

    def test_get_tasks_returns_list(self) -> None:
        assert isinstance(GeneratorTaskSource(count=3).get_tasks(), list)