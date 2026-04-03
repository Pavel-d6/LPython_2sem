from collections.abc import Callable
from typing import Any

from task import Task


class GeneratorTaskSource:
    """Источник задач, программно создающий задачи."""

    def __init__(
        self,
        count: int,
        factory: Callable[[int], Task] | None = None,
    ) -> None:
        if count <= 0:
            raise ValueError("count должен быть положительным")
        self._count = count
        self._factory: Callable[[int], Task] = factory or self._default_factory

    @staticmethod
    def _default_factory(index: int) -> Task:
        return Task(
            id=f"generated-{index}",
            description="проверить состояние ресурса",
            priority=(index % 10) + 1,
            payload=f"проверить состояние ресурса #{index}",
        )

    def get_tasks(self) -> list[Task]:
        return [self._factory(i) for i in range(self._count)]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(count={self._count})"