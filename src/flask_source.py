import json
import urllib.request
import urllib.error
from typing import Any

from task import Task


class FlaskApiTaskSource:
    """Источник задач, получающий задачи от Flask-сервера по HTTP."""

    def __init__(self, base_url: str = "http://localhost:5000") -> None:
        self._base_url = base_url.rstrip("/")

    def get_tasks(self) -> list[Task]:
        url = f"{self._base_url}/tasks"
        try:
            with urllib.request.urlopen(url) as response:
                body = response.read().decode("utf-8")
        except urllib.error.URLError as e:
            raise ConnectionError(
                f"Не удалось подключиться к серверу '{url}': {e.reason}"
            ) from e

        raw: Any = json.loads(body)

        if not isinstance(raw, list):
            raise ValueError("Сервер вернул неверный формат")

        return [
            Task(
                id=str(item["id"]),
                description=item["description"],
                priority=item["priority"],
                payload=item["payload"],
            )
            for item in raw
        ]

    @property
    def base_url(self) -> str:
        return self._base_url

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(base_url={self._base_url!r})"