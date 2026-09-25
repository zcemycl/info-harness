"""Diary root follows Lambda /tmp and an explicit override."""

from __future__ import annotations

from pathlib import Path

from tools.diary.default_diary_dir import diary_root
from tools.diary.relative_diary_path import relative_diary_path


def test_local_diary_root(monkeypatch) -> None:
    monkeypatch.delenv("AWS_LAMBDA_FUNCTION_NAME", raising=False)
    monkeypatch.delenv("DIARY_DIR", raising=False)
    assert diary_root() == Path("data/diary").resolve()


def test_lambda_diary_root_is_tmp(monkeypatch) -> None:
    monkeypatch.delenv("DIARY_DIR", raising=False)
    monkeypatch.setenv("AWS_LAMBDA_FUNCTION_NAME", "agentic-chat")
    assert diary_root() == Path("/tmp/diary")


def test_diary_dir_env_wins_on_lambda(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("AWS_LAMBDA_FUNCTION_NAME", "agentic-chat")
    monkeypatch.setenv("DIARY_DIR", str(tmp_path))
    assert diary_root() == tmp_path.resolve()


def test_relative_diary_path(tmp_path: Path) -> None:
    target = tmp_path / "run" / "note.json"
    target.parent.mkdir()
    target.write_text("{}", encoding="utf-8")
    assert relative_diary_path(target, tmp_path) == "run/note.json"
