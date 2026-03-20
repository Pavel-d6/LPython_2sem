from collections.abc import Callable
from typing import Any

from task import Task

class GeneratorTaskSource:
    """
    Источник задач, программно создающий задачи
    """

    def __init__(
        self,
        count: int,
        factory: Callable[[int], Task] | None = None,
    ) -> None:
        """
        Args:
            count: Количество задач для генерации.
            factory: Функция для создания задач.
        """
        if count <= 0:
            raise ValueError(f"count должен быть положительным")

        self._count = count
        self._factory: Callable[[int], Task] = factory or self._default_factory

    @staticmethod
    def _default_factory(index: int) -> Task:
        """Фабрика задач по умолчанию."""
        return Task(id=f"generated-{index}", payload=f"проверить состояние ресурса #{index}")

    def get_tasks(self) -> list[Task]:
        """
        Генерирует и возвращает список задач.
        """
        return [self._factory(i) for i in range(self._count)]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(count={self._count})"
