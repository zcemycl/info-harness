"""Append one message and refresh chat metadata."""

from __future__ import annotations

import json
from typing import Literal

from model.chat.chat_message import ChatMessage
from model.chat.chat_meta import ChatMeta
from tools.chat.object_key import object_key
from tools.chat.object_store import ObjectStore, open_object_store
from tools.chat.utc_now import utc_now


def append_message(
    chat_id: str,
    *,
    role: Literal["user", "assistant"],
    content: str,
    run_id: str | None = None,
) -> ChatMessage | None:
    """Append to history. Return ``None`` when the chat does not exist."""
    store = open_object_store()
    meta_raw = store.get_text(object_key("meta", chat_id=chat_id))
    if meta_raw is None:
        return None
    history_raw = store.get_text(object_key("history", chat_id=chat_id))
    payload = json.loads(history_raw or '{"messages":[]}')
    message = ChatMessage(
        role=role,
        content=content,
        ts=utc_now(),
        run_id=run_id,
    )
    messages = list(payload.get("messages", []))
    messages.append(message.model_dump())
    store.put_text(
        object_key("history", chat_id=chat_id),
        json.dumps({"messages": messages}),
    )
    _touch_meta(store, chat_id, meta_raw, role, content)
    return message


def _touch_meta(
    store: ObjectStore,
    chat_id: str,
    meta_raw: str,
    role: Literal["user", "assistant"],
    content: str,
) -> None:
    meta = ChatMeta.model_validate_json(meta_raw)
    title = meta.title
    if role == "user" and title == "New chat":
        title = content.strip().replace("\n", " ")[:80] or title
    updated = meta.model_copy(update={"title": title, "updated_at": utc_now()})
    store.put_text(object_key("meta", chat_id=chat_id), updated.model_dump_json())
