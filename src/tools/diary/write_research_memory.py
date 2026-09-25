"""Persist ResearchMemory snapshot under the diary tree."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from model.research.research_memory import ResearchMemory
from tools.diary.default_diary_dir import diary_root
from tools.diary.diary_folder import diary_folder
from tools.diary.relative_diary_path import relative_diary_path


def write_research_memory(
    memory: ResearchMemory,
    *,
    diary_dir: Path | None = None,
    name_prefix: str | None = None,
) -> str:
    """Write ``memory-<stamp>.json``; return its path relative to the diary root."""
    root = diary_root(diary_dir)
    folder = diary_folder(root, name_prefix)
    folder.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S")
    path = folder / f"memory-{stamp}-{uuid4().hex[:8]}.json"
    path.write_text(
        memory.model_dump_json(indent=2) + "\n",
        encoding="utf-8",
    )
    return relative_diary_path(path, root)
