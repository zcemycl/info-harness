"""Persist the ICD specialist final result under the diary folder."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from model.therapeutic_area.icd_specialist_result import IcdSpecialistResult
from tools.diary.default_diary_dir import DEFAULT_DIARY_DIR
from tools.diary.diary_folder import diary_folder


def write_icd_specialist_result(
    result: IcdSpecialistResult,
    *,
    diary_dir: Path = DEFAULT_DIARY_DIR,
    name_prefix: str | None = None,
) -> str:
    """Write ``final-<stamp>.json``; return its cwd-relative path."""
    root = diary_dir.expanduser().resolve()
    folder = diary_folder(root, name_prefix)
    folder.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S")
    path = folder / f"final-{stamp}-{uuid4().hex[:8]}.json"
    path.write_text(
        result.model_dump_json(indent=2) + "\n",
        encoding="utf-8",
    )
    return path.relative_to(Path.cwd().resolve()).as_posix()
