"""List chats from stored metadata."""

from __future__ import annotations

from model.chat.chat_meta import ChatMeta
from tools.chat.object_store import open_object_store


def list_chats() -> list[ChatMeta]:
    """Return chat metas, newest ``updated_at`` first."""
    store = open_object_store()
    metas: list[ChatMeta] = []
    for key in store.list_prefix("chats"):
        if not key.endswith("/meta.json"):
            continue
        raw = store.get_text(key)
        if raw:
            metas.append(ChatMeta.model_validate_json(raw))
    metas.sort(key=lambda item: item.updated_at, reverse=True)
    return metas
