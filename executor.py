import asyncio
from handlers.registry import HandlerRegistry
import logging

log = logging.getLogger(__name__)
 


class TaskExecutor:
    def __init__(self, queue: asyncio.Queue, registry: HandlerRegistry, workers: int = 3):
        self._queue = queue
        self._registry = registry
        self._workers_count = workers
        self._tasks: list[asyncio.Task] = []


    async def _worker(self):
        while True:
            task = await self._queue.get()  
            try:
                task.start()
                handler = self._registry.get(task.task_type)
                await handler.handle(task)
                task.complete()
            except Exception as e:
                log.error("Ошибка при обработке задачи %s: %s", task.id, e)
            finally:
                self._queue.task_done() 
                

    async def start(self):
        '''Запускает воркеры для обработки задач из очереди.'''
        for _ in range(self._workers_count):
            task = asyncio.create_task(self._worker())
            self._tasks.append(task)


    async def stop(self):
        '''Останавливает исполнителя, ожидая завершения текущих задач.'''
        await self._queue.join()  
        for task in self._tasks:
            task.cancel() 
            
        await asyncio.gather(*self._tasks, return_exceptions=True)
            

    async def __aenter__(self):
        await self.start()
        return self 


    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            log.error("Ошибка в executor: %s", exc_val)
        await self.stop()