"""Persist a full evidence value as a diary JSON artifact."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

from tools.diary.default_diary_dir import diary_root
from tools.diary.diary_folder import diary_folder
from tools.diary.relative_diary_path import relative_diary_path


def write_evidence_artifact(
    value: Any,
    *,
    run_id: str,
    meta: dict[str, Any] | None = None,
    diary_dir: Path | None = None,
) -> str:
    """Write ``{meta, value}`` under ``{run_id}/evidence/``."""
    root = diary_root(diary_dir)
    folder = diary_folder(root, f"{run_id.strip()}/evidence")
    folder.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S")
    path = folder / f"{stamp}-{uuid4().hex[:8]}.json"
    payload = {"meta": meta or {}, "value": value}
    path.write_text(json.dumps(payload, indent=2, default=str) + "\n", encoding="utf-8")
    return relative_diary_path(path, root)
