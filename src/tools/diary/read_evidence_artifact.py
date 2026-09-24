"""Read a diary evidence artifact with optional char window."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from tools.diary.default_diary_dir import DEFAULT_DIARY_DIR
from tools.diary.resolve_diary_path import resolve_diary_path


def read_evidence_artifact(
    path: str,
    *,
    offset: int = 0,
    limit_chars: int | None = None,
    diary_dir: Path = DEFAULT_DIARY_DIR,
) -> dict[str, Any]:
    """Load an evidence artifact; return meta + windowed text of the value."""
    resolved = resolve_diary_path(path, diary_dir=diary_dir)
    raw = json.loads(resolved.read_text(encoding="utf-8"))
    meta = raw.get("meta") if isinstance(raw, dict) else {}
    value = raw.get("value") if isinstance(raw, dict) else raw
    if isinstance(value, str):
        text = value
    else:
        text = json.dumps(value, indent=2, default=str)
    total = len(text)
    start = max(0, offset)
    default_limit = int(os.getenv("EVIDENCE_ARTIFACT_READ_CHARS", "4000"))
    limit = default_limit if limit_chars is None else max(1, limit_chars)
    window = text[start : start + limit]
    return {
        "path": path,
        "meta": meta or {},
        "total_chars": total,
        "offset": start,
        "limit_chars": limit,
        "next_offset": start + len(window) if start + len(window) < total else None,
        "text": window,
    }
