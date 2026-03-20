import uuid
from flask import Flask, jsonify, abort

app = Flask(__name__)


def _generate_tasks(count: int = 10) -> list[dict]:
    templates = [
        lambda i: {"action": "process_order",     "order_id": 1000 + i},
        lambda i: {"action": "send_notification", "user_id": i},
        lambda i: {"action": "recalculate_stats", "period": f"2024-Q{(i % 4) + 1}"},
        lambda i: {"action": "check_resource",    "resource": f"service-{i}"},
        lambda i: {"action": "process_incoming",  "source": f"webhook-{i}"},
    ]
    return [
        {
            "id": f"task-{i:03d}",
            "payload": templates[i % len(templates)](i),
        }
        for i in range(count)
    ]


@app.get("/tasks")
def get_tasks():
    """Возвращает список всех задач."""
    return jsonify(_generate_tasks())


@app.get("/tasks/<task_id>")
def get_task(task_id: str):
    """Возвращает одну задачу по id."""
    task = next((t for t in _generate_tasks() if t["id"] == task_id), None)
    if task is None:
        abort(404, description=f"Задача '{task_id}' не найдена")
    return jsonify(task)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
