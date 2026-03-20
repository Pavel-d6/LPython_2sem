from typing import Protocol, runtime_checkable

from task import Task


@runtime_checkable
class TaskSource(Protocol):
    """
    Протокол источника задач.
    """

    def get_tasks(self) -> list[Task]:
        """
        Возвращает список задач из источника
        """
        ...


def validate_source(source: object) -> TaskSource:
    """
    Runtime-проверка соответствия объекта контракту TaskSource.

    Args:
        source: Проверяемый объект.
    """
    if not isinstance(source, TaskSource):
        raise TypeError(
            f"Объект типа '{type(source).__name__}' не реализует протокол TaskSource. "
            f"Необходим метод get_tasks()."
        )
    return source  
