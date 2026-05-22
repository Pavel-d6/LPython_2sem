from protocol import TaskHandler, validate_handler
from typing import Dict

class HandlerRegistry:
    def __init__(self):
        self._handlers: Dict[str, TaskHandler] = {}

    def register(self, task_type: str, handler: TaskHandler) -> None:
        """Регистрирует обработчик для указанного типа задач."""
        self._handlers[task_type] = validate_handler(handler)



    def get(self, task_type: str) -> TaskHandler:
        """Получает обработчик для указанного типа задач, или 'default' если не найден."""
        handler = self._handlers.get(task_type) or self._handlers.get("default")
        if handler is None:
            raise KeyError("Обработчик не найден и 'default' не зарегистрирован")
        return handler