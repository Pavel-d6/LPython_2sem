import pytest

from task import Task


class TestTask:
    def test_create_valid_task(self) -> None:
        task = Task(id="task-1", payload="обработать заказ")
        assert task.id == "task-1"
        assert task.payload == "обработать заказ"

    def test_create_task_with_dict_payload(self) -> None:
        payload = {"action": "send_notification", "user_id": 42}
        task = Task(id="task-2", payload=payload)
        assert task.payload == payload

    def test_task_is_immutable(self) -> None:
        task = Task(id="task-1", payload="data")
        with pytest.raises(Exception):
            task.id = "other"  

    def test_empty_id_raises(self) -> None:
        with pytest.raises(ValueError, match="id должен быть непустой строкой"):
            Task(id="", payload="data")

    def test_non_string_id_raises(self) -> None:
        with pytest.raises(TypeError, match="id должен быть строкой"):
            Task(id=123, payload="data") 

    def test_none_payload_raises(self) -> None:
        with pytest.raises(ValueError, match="payload is None"):
            Task(id="task-1", payload=None)

    def test_tasks_equality(self) -> None:
        t1 = Task(id="x", payload="data")
        t2 = Task(id="x", payload="data")
        assert t1 == t2

    def test_tasks_inequality(self) -> None:
        t1 = Task(id="x", payload="data1")
        t2 = Task(id="x", payload="data2")
        assert t1 != t2
