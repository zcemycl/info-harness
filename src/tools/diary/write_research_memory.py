"""Persist ResearchMemory snapshot under the diary tree."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from model.research.research_memory import ResearchMemory
from tools.diary.default_diary_dir import DEFAULT_DIARY_DIR
from tools.diary.diary_folder import diary_folder


def write_research_memory(
    memory: ResearchMemory,
    *,
    diary_dir: Path = DEFAULT_DIARY_DIR,
    name_prefix: str | None = None,
) -> str:
    """Write ``memory-<stamp>.json``; return cwd-relative path."""
    root = diary_dir.expanduser().resolve()
    folder = diary_folder(root, name_prefix)
    folder.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S")
    path = folder / f"memory-{stamp}-{uuid4().hex[:8]}.json"
    path.write_text(
        memory.model_dump_json(indent=2) + "\n",
        encoding="utf-8",
    )
    return path.relative_to(Path.cwd().resolve()).as_posix()
