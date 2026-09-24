"""Persist a full evidence value as a diary JSON artifact."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

from tools.diary.default_diary_dir import DEFAULT_DIARY_DIR
from tools.diary.diary_folder import diary_folder


def write_evidence_artifact(
    value: Any,
    *,
    run_id: str,
    meta: dict[str, Any] | None = None,
    diary_dir: Path = DEFAULT_DIARY_DIR,
) -> str:
    """Write ``{meta, value}`` under ``data/diary/{run_id}/evidence/``; return path."""
    root = diary_dir.expanduser().resolve()
    folder = diary_folder(root, f"{run_id.strip()}/evidence")
    folder.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S")
    path = folder / f"{stamp}-{uuid4().hex[:8]}.json"
    payload = {"meta": meta or {}, "value": value}
    path.write_text(json.dumps(payload, indent=2, default=str) + "\n", encoding="utf-8")
    return path.relative_to(Path.cwd().resolve()).as_posix()
