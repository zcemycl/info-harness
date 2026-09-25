"""Persist run status and the run-id index."""

from __future__ import annotations

import json

from tools.chat.object_key import object_key
from tools.chat.object_store import open_object_store
from tools.chat.utc_now import utc_now


def put_run_status(
    chat_id: str,
    run_id: str,
    status: str,
    *,
    brief: str = "",
    error: str | None = None,
) -> None:
    """Write ``status.json`` and ``run-index/{run_id}.json``."""
    store = open_object_store()
    kept_brief = brief
    if not kept_brief:
        previous_raw = store.get_text(object_key("run_index", run_id=run_id))
        if previous_raw:
            kept_brief = str(json.loads(previous_raw).get("brief") or "")
    payload = {
        "chat_id": chat_id,
        "run_id": run_id,
        "status": status,
        "brief": kept_brief,
        "error": error,
        "updated_at": utc_now(),
    }
    text = json.dumps(payload)
    store.put_text(object_key("status", chat_id=chat_id, run_id=run_id), text)
    store.put_text(object_key("run_index", run_id=run_id), text)
