import pytest

from task import Task
from protocol import TaskSource, validate_source


class ValidSource:
    """Корректная реализация контракта."""
    def get_tasks(self) -> list[Task]:
        return [Task(id="t1", payload="data")]


class InvalidSource:
    """Объект без метода get_tasks."""
    def fetch(self) -> list[Task]:
        return []


class EmptySource:
    """Корректный источник, возвращающий пустой список."""
    def get_tasks(self) -> list[Task]:
        return []


class TestTaskSourceProtocol:
    def test_valid_source_is_instance_of_protocol(self) -> None:
        source = ValidSource()
        assert isinstance(source, TaskSource)

    def test_invalid_source_is_not_instance_of_protocol(self) -> None:
        source = InvalidSource()
        assert not isinstance(source, TaskSource)

    def test_empty_source_satisfies_protocol(self) -> None:
        source = EmptySource()
        assert isinstance(source, TaskSource)

    def test_validate_source_accepts_valid(self) -> None:
        source = ValidSource()
        result = validate_source(source)
        assert result is source

    def test_validate_source_rejects_invalid(self) -> None:
        source = InvalidSource()
        with pytest.raises(TypeError, match="не реализует протокол TaskSource"):
            validate_source(source)

    def test_validate_source_rejects_plain_object(self) -> None:
        with pytest.raises(TypeError):
            validate_source(object())

    def test_validate_source_rejects_string(self) -> None:
        with pytest.raises(TypeError):
            validate_source("not a source")

    def test_validate_source_error_message_contains_class_name(self) -> None:
        source = InvalidSource()
        with pytest.raises(TypeError, match="InvalidSource"):
            validate_source(source)
