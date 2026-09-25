"""Resolve which chat owns a run id."""

from __future__ import annotations

import json

from tools.chat.object_key import object_key
from tools.chat.object_store import open_object_store


def chat_id_for_run(run_id: str) -> str | None:
    """Return the chat id stored in the run index, or ``None``."""
    raw = open_object_store().get_text(object_key("run_index", run_id=run_id))
    if raw is None:
        return None
    chat_id = json.loads(raw).get("chat_id")
    if not chat_id:
        return None
    return str(chat_id)
