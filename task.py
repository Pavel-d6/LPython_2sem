from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Task:
    """
    id: Уникальный идентификатор задачи
    payload: Произвольные данные задачи
    """

    id: str
    payload: Any

    def __post_init__(self) -> None:
        if not isinstance(self.id, str):
            raise TypeError(f"id должен быть строкой, получено")
        if not self.id:
            raise ValueError("id должен быть непустой строкой")
        if self.payload is None:
            raise ValueError("payload is None")
