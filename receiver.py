from protocol import TaskSource, validate_source
from task import Task


class TaskReceiver:

    def __init__ (self):
        self._sources: list[TaskSource] = []



    def register(self, source: object) -> None:
        """
        Регистрирует источник задач после runtime-проверки контракта.
        """
        validated = validate_source(source)
        self._sources.append(validated)

    def collect_all(self) -> list[Task]:
        """
        Собирает задачи из всех зарегистрированных источников.
        """
        result: list[Task] = []
        for source in self._sources:
            result.extend(source.get_tasks())
        return result

    def collect_from(self, source: object) -> list[Task]:
        """
        Получает задачи из одного источника с предварительной проверкой контракта.
        """
        validated = validate_source(source)
        return validated.get_tasks()

    @property
    def source_count(self) -> int:
        """Количество зарегистрированных источников."""
        return len(self._sources)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(sources={self._sources!r})"

