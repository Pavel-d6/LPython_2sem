
import pytest
from task import Task
from protocol import TaskSource, validate_source


class ValidSource:
    def get_tasks(self) -> list[Task]:
        return [Task(id="t1", description="тест", priority=5, payload="data")]

class InvalidSource:
    def fetch(self) -> list[Task]:
        return []

class EmptySource:
    def get_tasks(self) -> list[Task]:
        return []


class TestTaskSourceProtocol:
    def test_valid_source_is_instance_of_protocol(self) -> None:
        assert isinstance(ValidSource(), TaskSource)

    def test_invalid_source_is_not_instance_of_protocol(self) -> None:
        assert not isinstance(InvalidSource(), TaskSource)

    def test_empty_source_satisfies_protocol(self) -> None:
        assert isinstance(EmptySource(), TaskSource)

    def test_validate_source_accepts_valid(self) -> None:
        s = ValidSource()
        assert validate_source(s) is s

    def test_validate_source_rejects_invalid(self) -> None:
        with pytest.raises(TypeError, match="не реализует протокол TaskSource"):
            validate_source(InvalidSource())

    def test_validate_source_rejects_plain_object(self) -> None:
        with pytest.raises(TypeError):
            validate_source(object())

    def test_validate_source_rejects_string(self) -> None:
        with pytest.raises(TypeError):
            validate_source("not a source")

    def test_error_message_contains_class_name(self) -> None:
        with pytest.raises(TypeError, match="InvalidSource"):
            validate_source(InvalidSource())