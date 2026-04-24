from typing import Generator
from task import Task, Status

class TaskQueue:
    def __init__(self, tasks: list[Task] | None = None) -> None:
        self._tasks: list[Task] = list(tasks) if tasks else []

    def add(self, task: Task) -> None:
        if not isinstance(task, Task):
            raise TypeError(f"Ожидается Task, получено: {type(task).__name__}")
        self._tasks.append(task)
    
    def __iter__(self)  -> Generator[Task, None, None]:
        """
        Генераторная функция
        Каждый вызов создаёт новый генератор с начала списка для поатороного обхода
        """
        for task in self._tasks:
            yield task

    def __len__(self) -> int:
        """Количество задач в очереди."""
        return len(self._tasks)


    def __contains__(self, task: object):
        return task in self._tasks

    def filter_by_status(self, status: Status) -> Generator[Task, None, None]:
        """
        Ленивый фильтр по статусу задачи
 
        Args:
            status: Статус для фильтрации
        """
        for task in self._tasks:
            if task.status == status:
                yield task


    def filter_by_priority(self, min_priority: int, max_priority: int = 10) -> Generator[Task, None, None]:
        """
        Ленивый фильтр по приоритету задачи.
        Args:
            min_priority: Минимальный приоритет
            max_priority: Максимальный приоритет
        """
        for task in self._tasks:
            if min_priority <= task.priority <= max_priority:
                yield task
    
    def __repr__(self) -> str:
        return f"TaskQueue(size={len(self._tasks)})"
