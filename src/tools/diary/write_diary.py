"""Write a structured research diary entry as JSON."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from model.research.diary_entry import DiaryEntry
from tools.diary.default_diary_dir import DEFAULT_DIARY_DIR
from tools.diary.diary_folder import diary_folder


def write_diary(
    entry: DiaryEntry,
    *,
    diary_dir: Path = DEFAULT_DIARY_DIR,
    name_prefix: str | None = None,
) -> str:
    """Append ``entry`` as a new JSON diary file; return its cwd-relative path.

    Args:
        entry: Structured loop feedback for the next planner.
        diary_dir: Root diary directory (created if missing).
        name_prefix: Optional relative subfolder under ``diary_dir``
            (e.g. ``{run_id}/outer`` or ``{run_id}/fda``).
    """
    root = diary_dir.expanduser().resolve()
    folder = diary_folder(root, name_prefix)
    folder.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S")
    path = folder / f"{stamp}-{uuid4().hex[:8]}.json"
    path.write_text(
        entry.model_dump_json(indent=2) + "\n",
        encoding="utf-8",
    )
    return path.relative_to(Path.cwd().resolve()).as_posix()
