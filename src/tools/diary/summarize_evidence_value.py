"""Build a capped summary and optional diary artifact for an evidence value."""

from __future__ import annotations

import json
import os
from typing import Any

from pydantic import BaseModel

from tools.diary.write_evidence_artifact import write_evidence_artifact


def summarize_evidence_value(
    value: Any,
    *,
    run_id: str,
    meta: dict[str, Any] | None = None,
    max_chars: int | None = None,
) -> tuple[str, str | None, int]:
    """Return ``(summary, artifact_path|None, total_chars)``.

    Writes a diary artifact when the full text exceeds ``max_chars``.
    """
    text = _stringify(value)
    total = len(text)
    limit = (
        max_chars
        if max_chars is not None
        else int(os.getenv("EVIDENCE_SUMMARY_MAX_CHARS", "600"))
    )
    if total <= limit:
        return text, None, total
    path = write_evidence_artifact(value, run_id=run_id, meta=meta)
    head = text[: max(0, limit - 80)].rstrip()
    summary = f"{head}…[+{total - len(head)} chars; artifact={path}]"
    return summary, path, total


def _stringify(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, BaseModel):
        return json.dumps(value.model_dump(mode="json"), default=str)
    if hasattr(value, "model_dump"):
        # type: ignore[union-attr]
        return json.dumps(value.model_dump(mode="json"), default=str)
    return json.dumps(value, default=str)
