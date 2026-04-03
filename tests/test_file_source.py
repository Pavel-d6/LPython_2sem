
import json
import pytest
from pathlib import Path

from task import Task
from protocol import TaskSource
from src.sourse_from_file import FileTaskSource


def make_json(tmp_path: Path, data: list) -> Path:
    f = tmp_path / "tasks.json"
    f.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return f


VALID_ITEM = {"id": "t1", "description": "тест", "priority": 3, "payload": "данные"}


class TestFileTaskSource:
    def test_load_tasks_from_valid_file(self, tmp_path: Path) -> None:
        data = [
            {"id": "t1", "description": "обработать заказ",   "priority": 5, "payload": "x"},
            {"id": "t2", "description": "отправить уведомление", "priority": 3, "payload": "y"},
        ]
        tasks = FileTaskSource(make_json(tmp_path, data)).get_tasks()
        assert len(tasks) == 2
        assert tasks[0].id == "t1"
        assert tasks[1].id == "t2"

    def test_load_tasks_with_dict_payload(self, tmp_path: Path) -> None:
        data = [{"id": "t1", "description": "тест", "priority": 1, "payload": {"action": "check"}}]
        tasks = FileTaskSource(make_json(tmp_path, data)).get_tasks()
        assert tasks[0].payload == {"action": "check"}

    def test_load_empty_file(self, tmp_path: Path) -> None:
        f = tmp_path / "empty.json"
        f.write_text("[]", encoding="utf-8")
        assert FileTaskSource(f).get_tasks() == []

    def test_file_not_found_raises(self) -> None:
        with pytest.raises(FileNotFoundError):
            FileTaskSource("/nonexistent/tasks.json")

    def test_invalid_json_structure_raises(self, tmp_path: Path) -> None:
        f = tmp_path / "bad.json"
        f.write_text('{"id": "t1"}', encoding="utf-8")
        with pytest.raises(ValueError, match="массив JSON"):
            FileTaskSource(f).get_tasks()

    def test_missing_description_raises(self, tmp_path: Path) -> None:
        data = [{"id": "t1", "priority": 3, "payload": "x"}]
        with pytest.raises(ValueError, match="'description'"):
            FileTaskSource(make_json(tmp_path, data)).get_tasks()

    def test_missing_priority_raises(self, tmp_path: Path) -> None:
        data = [{"id": "t1", "description": "тест", "payload": "x"}]
        with pytest.raises(ValueError, match="'priority'"):
            FileTaskSource(make_json(tmp_path, data)).get_tasks()

    def test_satisfies_task_source_protocol(self, tmp_path: Path) -> None:
        f = tmp_path / "tasks.json"
        f.write_text("[]", encoding="utf-8")
        assert isinstance(FileTaskSource(f), TaskSource)

    def test_repr_contains_class_name(self, tmp_path: Path) -> None:
        f = tmp_path / "tasks.json"
        f.write_text("[]", encoding="utf-8")
        assert "FileTaskSource" in repr(FileTaskSource(f))