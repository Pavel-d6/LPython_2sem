import asyncio
import json
import logging
import tempfile
import os

from receiver import TaskReceiver
from executor import TaskExecutor
from handlers.registry import HandlerRegistry
from handlers.default import DefaultHandler
from src.generator_source import GeneratorTaskSource
from src.sourse_from_file import FileTaskSource
from src.flask_source import FlaskApiTaskSource

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)


async def main() -> None:
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8")
    json.dump([
        {"id": "file-1", "description": "задача из файла 1", "priority": 7, "payload": "alpha"},
        {"id": "file-2", "description": "задача из файла 2", "priority": 2, "payload": "beta"},
    ], tmp, ensure_ascii=False)
    tmp.close()

    receiver = TaskReceiver()
    receiver.register(GeneratorTaskSource(count=4))
    receiver.register(FileTaskSource(tmp.name))
    try:
        flask = FlaskApiTaskSource("http://localhost:5001")
        flask.get_tasks()
        receiver.register(flask)
    except ConnectionError:
        pass

    tasks = receiver.collect_all()

    queue: asyncio.Queue = asyncio.Queue()
    for task in tasks:
        queue.put_nowait(task)

    registry = HandlerRegistry()
    registry.register("default", DefaultHandler())

    async with TaskExecutor(queue, registry, workers=3):
        pass

    os.unlink(tmp.name)


if __name__ == "__main__":
    asyncio.run(main())
