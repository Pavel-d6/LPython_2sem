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


@runtime_checkable
class TaskHandler(Protocol):
    """
    Протокол обработчика задач.
    """

    async def handle(self, task: Task) -> None:
        """
        Асинхронно обрабатывает задачу.

        Args:
            task: Задача для обработки.
        """
        ...

def validate_handler(handler: object) -> TaskHandler:
    """
    Runtime-проверка соответствия объекта контракту TaskHandler.

    Args:
        handler: Проверяемый объект.
    """
    if not isinstance(handler, TaskHandler):
        raise TypeError(
            f"Объект типа '{type(handler).__name__}' не реализует протокол TaskHandler. "
            f"Необходим асинхронный метод handle(task: Task) -> None."
        )
    return handler