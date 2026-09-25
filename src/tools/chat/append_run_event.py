"""Append one run event line under a process lock."""

from __future__ import annotations

import threading

from model.chat.run_event import RunEvent
from tools.chat.object_key import object_key
from tools.chat.object_store import open_object_store

_LOCK = threading.Lock()


def append_run_event(event: RunEvent) -> RunEvent:
    """Assign ``seq`` and append one JSON line to ``events.jsonl``."""
    key = object_key("events", chat_id=event.chat_id, run_id=event.run_id)
    with _LOCK:
        store = open_object_store()
        existing = store.get_text(key) or ""
        seq = len([line for line in existing.splitlines() if line.strip()]) + 1
        written = event.model_copy(update={"seq": seq})
        body = existing
        if body and not body.endswith("\n"):
            body += "\n"
        body += written.model_dump_json() + "\n"
        store.put_text(key, body)
        return written
