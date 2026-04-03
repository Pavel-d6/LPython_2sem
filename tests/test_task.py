"""Тесты для модели Task — Лабораторная работа №2."""

import pytest
from datetime import datetime

from task import Task, Status
from exceptions import TaskValidationError, InvalidStatusTransitionError, InvalidPriorityError


def make_task(**kwargs) -> Task:
    defaults = dict(id="t-1", description="тестовая задача", priority=5, payload="data")
    return Task(**{**defaults, **kwargs})


class TestTaskCreation:
    def test_create_valid_task(self) -> None:
        t = make_task()
        assert t.id == "t-1"
        assert t.description == "тестовая задача"
        assert t.priority == 5
        assert t.payload == "data"

    def test_initial_status_is_pending(self) -> None:
        assert make_task().status == Status.PENDING

    def test_created_at_is_datetime(self) -> None:
        assert isinstance(make_task().created_at, datetime)

    def test_is_ready_true_when_pending(self) -> None:
        assert make_task().is_ready is True

    def test_empty_id_raises(self) -> None:
        with pytest.raises(TaskValidationError):
            make_task(id="")

    def test_non_string_id_raises(self) -> None:
        with pytest.raises(TypeError):
            make_task(id=123)  # type: ignore[arg-type]

    def test_none_payload_raises(self) -> None:
        with pytest.raises(TaskValidationError):
            make_task(payload=None)


class TestValidatedString:
    def test_set_valid_description(self) -> None:
        t = make_task()
        t.description = "новое описание"
        assert t.description == "новое описание"

    def test_empty_description_raises(self) -> None:
        with pytest.raises(TaskValidationError):
            make_task(description="")

    def test_whitespace_description_raises(self) -> None:
        with pytest.raises(TaskValidationError):
            make_task(description="   ")

    def test_non_string_description_raises(self) -> None:
        with pytest.raises(TypeError):
            make_task(description=123)  # type: ignore[arg-type]


class TestValidatedPriority:
    def test_set_valid_priority(self) -> None:
        t = make_task()
        t.priority = 8
        assert t.priority == 8

    def test_priority_min_boundary(self) -> None:
        assert make_task(priority=1).priority == 1

    def test_priority_max_boundary(self) -> None:
        assert make_task(priority=10).priority == 10

    def test_priority_too_low_raises(self) -> None:
        with pytest.raises(InvalidPriorityError):
            make_task(priority=0)

    def test_priority_too_high_raises(self) -> None:
        with pytest.raises(InvalidPriorityError):
            make_task(priority=11)

    def test_non_int_priority_raises(self) -> None:
        with pytest.raises(TypeError):
            make_task(priority="high")  # type: ignore[arg-type]


class TestReadOnlyProperties:
    def test_id_is_readonly(self) -> None:
        t = make_task()
        with pytest.raises(AttributeError):
            t.id = "other"  # type: ignore[misc]

    def test_status_is_readonly(self) -> None:
        t = make_task()
        with pytest.raises(AttributeError):
            t.status = Status.DONE  # type: ignore[misc]

    def test_created_at_is_readonly(self) -> None:
        t = make_task()
        with pytest.raises(AttributeError):
            t.created_at = datetime.now()  # type: ignore[misc]

    def test_payload_is_readonly(self) -> None:
        t = make_task()
        with pytest.raises(AttributeError):
            t.payload = "other"  # type: ignore[misc]


class TestStatusTransitions:
    def test_pending_to_in_progress(self) -> None:
        t = make_task()
        t.start()
        assert t.status == Status.IN_PROGRESS

    def test_in_progress_to_done(self) -> None:
        t = make_task()
        t.start()
        t.complete()
        assert t.status == Status.DONE

    def test_is_ready_false_after_start(self) -> None:
        t = make_task()
        t.start()
        assert t.is_ready is False

    def test_complete_from_pending_raises(self) -> None:
        with pytest.raises(InvalidStatusTransitionError):
            make_task().complete()

    def test_start_from_in_progress_raises(self) -> None:
        t = make_task()
        t.start()
        with pytest.raises(InvalidStatusTransitionError):
            t.start()

    def test_start_from_done_raises(self) -> None:
        t = make_task()
        t.start()
        t.complete()
        with pytest.raises(InvalidStatusTransitionError):
            t.start()

    def test_complete_from_done_raises(self) -> None:
        t = make_task()
        t.start()
        t.complete()
        with pytest.raises(InvalidStatusTransitionError):
            t.complete()