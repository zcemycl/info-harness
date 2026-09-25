"""Load a chat transcript."""

from __future__ import annotations

import json

from model.chat.chat_message import ChatMessage
from tools.chat.object_key import object_key
from tools.chat.object_store import open_object_store


def load_history(chat_id: str) -> list[ChatMessage] | None:
    """Return messages, or ``None`` when the chat does not exist."""
    store = open_object_store()
    if store.get_text(object_key("meta", chat_id=chat_id)) is None:
        return None
    raw = store.get_text(object_key("history", chat_id=chat_id)) or '{"messages":[]}'
    payload = json.loads(raw)
    return [ChatMessage.model_validate(item) for item in payload.get("messages", [])]
