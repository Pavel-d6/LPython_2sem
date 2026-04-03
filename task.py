
from datetime import datetime
from enum import Enum
from typing import Any

from exceptions import TaskValidationError, InvalidStatusTransitionError, InvalidPriorityError
from descriptors import ValidatedString, ValidatedPriority


class Status(Enum):
    """Жизненный цикл задачи"""
    PENDING     = "pending"
    IN_PROGRESS = "in_progress"
    DONE        = "done"


_ALLOWED_TRANSITIONS: dict[Status, Status] = {
    Status.PENDING:     Status.IN_PROGRESS,
    Status.IN_PROGRESS: Status.DONE,
}


class Task:
    """
    Модель задачи.
    """

    description = ValidatedString()
    priority    = ValidatedPriority()

    def __init__(
        self,
        id: str,
        description: str,
        priority: int,
        payload: Any,
    ) -> None:
        if not isinstance(id, str):
            raise TypeError(f"'id' должен быть строкой, получено: {type(id).__name__}")
        if not id.strip():
            raise TaskValidationError("'id' не может быть пустым")
        if payload is None:
            raise TaskValidationError("'payload' не может быть None")

        self._id         = id
        self._payload    = payload
        self._status     = Status.PENDING
        self._created_at = datetime.now()

        self.description = description
        self.priority    = priority

    @property
    def id(self) -> str:
        """Уникальный идентификатор задачи. Только для чтения."""
        return self._id

    @property
    def payload(self) -> Any:
        """Данные задачи. Только для чтения."""
        return self._payload

    @property
    def status(self) -> Status:
        """Текущий статус. Изменяется только через start() и complete()."""
        return self._status

    @property
    def created_at(self) -> datetime:
        """Время создания задачи. Только для чтения."""
        return self._created_at

    @property
    def is_ready(self) -> bool:
        """True если задача ожидает выполнения (статус PENDING)."""
        return self._status == Status.PENDING

    def start(self) -> None:
        """PENDING → IN_PROGRESS."""
        self._transition_to(Status.IN_PROGRESS)

    def complete(self) -> None:
        """IN_PROGRESS → DONE."""
        self._transition_to(Status.DONE)

    def _transition_to(self, new_status: Status) -> None:
        allowed = _ALLOWED_TRANSITIONS.get(self._status)
        if allowed != new_status:
            raise InvalidStatusTransitionError(
                f"Недопустимый переход: {self._status.value} → {new_status.value}"
            )
        self._status = new_status


    def __repr__(self) -> str:
        return (
            f"Task(id={self.id!r}, description={self.description!r}, "
            f"priority={self.priority}, status={self._status.value}, "
            f"payload={self.payload!r})"
        )