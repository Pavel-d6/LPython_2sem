import json
from pathlib import Path
from typing import Any

from task import Task


class FileTaskSource:
    """Источник задач, загружающий данные из JSON-файла."""

    def __init__(self, filepath: str | Path) -> None:
        self._filepath = Path(filepath)
        if not self._filepath.exists():
            raise FileNotFoundError(f"Файл не найден: {self._filepath}")

    def get_tasks(self) -> list[Task]:
        raw: Any = json.loads(self._filepath.read_text(encoding="utf-8"))

        if not isinstance(raw, list):
            raise ValueError(f"Файл '{self._filepath}' должен содержать массив JSON")

        tasks: list[Task] = []
        for i, item in enumerate(raw):
            if not isinstance(item, dict):
                raise ValueError(f"Элемент [{i}] должен быть объектом JSON")
            for field in ("id", "description", "priority", "payload"):
                if field not in item:
                    raise ValueError(
                        f"Элемент [{i}] должен содержать поле '{field}', получено: {list(item.keys())}"
                    )
            tasks.append(Task(
                id=str(item["id"]),
                description=item["description"],
                priority=item["priority"],
                payload=item["payload"],
            ))

        return tasks

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(filepath={self._filepath!r})"