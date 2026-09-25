"""S3 / local keys for chats and runs."""

from __future__ import annotations

from typing import Literal

ObjectKind = Literal["meta", "history", "status", "events", "result", "run_index"]


def object_key(
    kind: ObjectKind,
    *,
    chat_id: str = "",
    run_id: str = "",
) -> str:
    """Return a relative object key for ``kind``."""
    if kind == "run_index":
        return f"run-index/{run_id}.json"
    if kind == "meta":
        return f"chats/{chat_id}/meta.json"
    if kind == "history":
        return f"chats/{chat_id}/history.json"
    if kind == "status":
        return f"chats/{chat_id}/runs/{run_id}/status.json"
    if kind == "events":
        return f"chats/{chat_id}/runs/{run_id}/events.jsonl"
    return f"chats/{chat_id}/runs/{run_id}/result.json"
