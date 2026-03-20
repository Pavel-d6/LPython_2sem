
import json
import pytest
from pathlib import Path

from src.sourse_from_file import FileTaskSource
from task import Task
from protocol import TaskSource


class TestFileTaskSource:
    def test_load_tasks_from_valid_file(self, tmp_path: Path) -> None:
        data = [
            {"id": "t1", "payload": "обработать заказ"},
            {"id": "t2", "payload": "отправить уведомление"},
        ]
        f = tmp_path / "tasks.json"
        f.write_text(json.dumps(data), encoding="utf-8")

        source = FileTaskSource(f)
        tasks = source.get_tasks()

        assert len(tasks) == 2
        assert tasks[0] == Task(id="t1", payload="обработать заказ")
        assert tasks[1] == Task(id="t2", payload="отправить уведомление")

    def test_load_tasks_with_dict_payload(self, tmp_path: Path) -> None:
        data = [{"id": "t1", "payload": {"action": "check", "target": "db"}}]
        f = tmp_path / "tasks.json"
        f.write_text(json.dumps(data), encoding="utf-8")

        tasks = FileTaskSource(f).get_tasks()
        assert tasks[0].payload == {"action": "check", "target": "db"}

    def test_load_empty_file(self, tmp_path: Path) -> None:
        f = tmp_path / "empty.json"
        f.write_text("[]", encoding="utf-8")

        tasks = FileTaskSource(f).get_tasks()
        assert tasks == []

    def test_file_not_found_raises(self) -> None:
        with pytest.raises(FileNotFoundError):
            FileTaskSource("/nonexistent/path/tasks.json")

    def test_invalid_json_structure_raises(self, tmp_path: Path) -> None:
        f = tmp_path / "bad.json"
        f.write_text('{"id": "t1", "payload": "data"}', encoding="utf-8")  # dict, not list

        with pytest.raises(ValueError, match="массив JSON"):
            FileTaskSource(f).get_tasks()

    def test_missing_id_field_raises(self, tmp_path: Path) -> None:
        f = tmp_path / "tasks.json"
        f.write_text(json.dumps([{"payload": "data"}]), encoding="utf-8")

        with pytest.raises(ValueError, match="'id'"):
            FileTaskSource(f).get_tasks()

    def test_missing_payload_field_raises(self, tmp_path: Path) -> None:
        f = tmp_path / "tasks.json"
        f.write_text(json.dumps([{"id": "t1"}]), encoding="utf-8")

        with pytest.raises(ValueError, match="'payload'"):
            FileTaskSource(f).get_tasks()

    def test_satisfies_task_source_protocol(self, tmp_path: Path) -> None:
        f = tmp_path / "tasks.json"
        f.write_text("[]", encoding="utf-8")
        assert isinstance(FileTaskSource(f), TaskSource)

    def test_repr_contains_path(self, tmp_path: Path) -> None:
        f = tmp_path / "tasks.json"
        f.write_text("[]", encoding="utf-8")
        source = FileTaskSource(f)
        assert "FileTaskSource" in repr(source)
