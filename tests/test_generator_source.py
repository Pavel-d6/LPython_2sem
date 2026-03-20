import pytest

from src.generator_source import GeneratorTaskSource
from task import Task
from protocol import TaskSource

class TestGeneratorTaskSource:
    def test_generates_correct_count(self) -> None:
        source = GeneratorTaskSource(count=5)
        tasks = source.get_tasks()
        assert len(tasks) == 5

    def test_default_factory_produces_valid_tasks(self) -> None:
        source = GeneratorTaskSource(count=3)
        tasks = source.get_tasks()
        for task in tasks:
            assert isinstance(task, Task)
            assert task.id
            assert task.payload

    def test_default_ids_are_unique(self) -> None:
        tasks = GeneratorTaskSource(count=10).get_tasks()
        ids = [t.id for t in tasks]
        assert len(set(ids)) == len(ids)

    def test_custom_factory_is_used(self) -> None:
        factory = lambda i: Task(id=f"custom-{i}", payload=f"job-{i}")
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
        tasks = GeneratorTaskSource(count=3).get_tasks()
        assert isinstance(tasks, list)

    def test_single_task_generation(self) -> None:
        tasks = GeneratorTaskSource(count=1).get_tasks()
        assert len(tasks) == 1
