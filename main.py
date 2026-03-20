from src.flask_source import FlaskApiTaskSource
from receiver import TaskReceiver

receiver = TaskReceiver()
receiver.register(FlaskApiTaskSource("http://localhost:5001"))

tasks = receiver.collect_all()
for task in tasks:
    print(task)