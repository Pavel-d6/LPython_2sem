import json, tempfile, os
from task import Task, Status
from exceptions import  InvalidStatusTransitionError
from receiver import TaskReceiver
from Task_queue import TaskQueue
from src.sourse_from_file import FileTaskSource
from src.generator_source import GeneratorTaskSource
from src.flask_source import FlaskApiTaskSource


def sep(title): print(f"\n--- {title} ---")




t = Task(id="t-1", description="обработать заказ", priority=5, payload={"order_id": 42})

sep("Статус-машина")
t.start(); print(f"после start:    {t.status.value}")
t.complete(); print(f"после complete: {t.status.value}")
try: t.start()
except InvalidStatusTransitionError as e: print(f"done→start: {e}")


# FileTaskSource
sep("FileTaskSource")
with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as f:
    json.dump([
        {"id": "f-1", "description": "задача из файла 1", "priority": 3, "payload": "a"},
        {"id": "f-2", "description": "задача из файла 2", "priority": 7, "payload": "b"},
    ], f, ensure_ascii=False)
    tmp = f.name
for t in FileTaskSource(tmp).get_tasks(): print(t)
os.unlink(tmp)


sep("GeneratorTaskSource — дефолтная фабрика")
for t in GeneratorTaskSource(count=3).get_tasks(): print(t)

sep("GeneratorTaskSource — кастомная фабрика")
factory = lambda i: Task(id=f"order-{i}", description=f"заказ #{i}", priority=i+1, payload=i)
for t in GeneratorTaskSource(count=3, factory=factory).get_tasks(): print(t)


sep("FlaskApiTaskSource")
try:
    tasks = FlaskApiTaskSource("http://localhost:5001").get_tasks()
    for t in tasks[:3]: print(t)
    print("...")
except ConnectionError as e: print(f"сервер недоступен: {e}")


sep("TaskReceiver")
receiver = TaskReceiver()
receiver.register(GeneratorTaskSource(count=2))
try: receiver.register(FlaskApiTaskSource("http://localhost:5001"))
except Exception: pass
print(f"источников: {receiver.source_count}, задач: {len(receiver.collect_all())}")



sep("TaskQueue")
tasks = [
    Task(id="q-1", description="задача 1", priority=3, payload="a"),
    Task(id="q-2", description="задача 2", priority=8, payload="b"),
    Task(id="q-3", description="задача 3", priority=5, payload="c"),
]
tasks[1].start()

queue = TaskQueue(tasks)
print("все задачи:")
for t in queue: print(f"  {t.id} [{t.status.value}] priority={t.priority}")

print("повторный обход:")
for t in queue: print(f"  {t.id}")

print("filter_by_status(PENDING):")
for t in queue.filter_by_status(Status.PENDING): print(f"  {t.id}")

print("filter_by_priority(min=5):")
for t in queue.filter_by_priority(min_priority=5): print(f"  {t.id} priority={t.priority}")

print(f"sum priority: {sum(t.priority for t in queue)}")