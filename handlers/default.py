import asyncio
import random
import logging
from task import Task

log = logging.getLogger(__name__)

class DefaultHandler:
    """Обработчик задач по умолчанию."""

    async def handle(self, task: Task) -> None:
        """Асинхронно обрабатывает задачу."""
        duration = round(random.uniform(0.1, 3.0), 2)
        log.info("Задача %s запущена, время выполнения: %ss", task.id, duration)
        await asyncio.sleep(duration)
        log.info("Задача %s выполнена", task.id)