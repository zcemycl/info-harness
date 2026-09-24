"""Read a structured research diary entry from disk."""

from __future__ import annotations

from pathlib import Path

from model.research.diary_entry import DiaryEntry
from tools.diary.default_diary_dir import DEFAULT_DIARY_DIR
from tools.diary.resolve_diary_path import resolve_diary_path


def read_diary(
    path: str,
    *,
    diary_dir: Path = DEFAULT_DIARY_DIR,
) -> DiaryEntry:
    """Load and validate a diary JSON file under ``diary_dir``.

    Args:
        path: Diary file path (absolute, cwd-relative, or under diary_dir).
        diary_dir: Directory that diary files must stay inside.
    """
    resolved = resolve_diary_path(path, diary_dir=diary_dir)
    return DiaryEntry.model_validate_json(resolved.read_text(encoding="utf-8"))
