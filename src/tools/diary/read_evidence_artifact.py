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
    meta, text = _body(raw)
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


def _body(raw: Any) -> tuple[dict[str, Any], str]:
    """Window an evidence ``value`` or a stage-answer ``answer`` field."""
    if not isinstance(raw, dict):
        return {}, json.dumps(raw, indent=2, default=str)
    if "value" in raw:
        value = raw.get("value")
        meta_raw = raw.get("meta")
        meta = meta_raw if isinstance(meta_raw, dict) else {}
        if isinstance(value, str):
            return meta, value
        return meta, json.dumps(value, indent=2, default=str)
    if isinstance(raw.get("answer"), str) and "agent" in raw:
        return (
            {
                "agent": raw.get("agent"),
                "status": raw.get("status"),
                "run_id": raw.get("run_id"),
                "loop": raw.get("loop"),
                "path": raw.get("path"),
            },
            raw["answer"],
        )
    return {}, json.dumps(raw, indent=2, default=str)
