"""S3 / local keys for chats and runs, scoped to one Cognito user."""

from __future__ import annotations

from typing import Literal

from tools.chat.bind_chat_owner import current_chat_owner

ObjectKind = Literal["meta", "history", "status", "events", "result", "run_index"]


def object_key(
    kind: ObjectKind,
    *,
    chat_id: str = "",
    run_id: str = "",
) -> str:
    """Return a relative object key under the bound Cognito user."""
    owner = current_chat_owner()
    base = f"users/{owner}"
    if kind == "run_index":
        return f"{base}/run-index/{run_id}.json"
    if kind == "meta":
        return f"{base}/chats/{chat_id}/meta.json"
    if kind == "history":
        return f"{base}/chats/{chat_id}/history.json"
    if kind == "status":
        return f"{base}/chats/{chat_id}/runs/{run_id}/status.json"
    if kind == "events":
        return f"{base}/chats/{chat_id}/runs/{run_id}/events.jsonl"
    return f"{base}/chats/{chat_id}/runs/{run_id}/result.json"
