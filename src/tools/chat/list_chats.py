"""List chats from stored metadata."""

from __future__ import annotations

from model.chat.chat_meta import ChatMeta
from tools.chat.bind_chat_owner import current_chat_owner
from tools.chat.object_store import open_object_store


def list_chats() -> list[ChatMeta]:
    """Return this user's chat metas, newest ``updated_at`` first."""
    store = open_object_store()
    prefix = f"users/{current_chat_owner()}/chats"
    metas: list[ChatMeta] = []
    for key in store.list_prefix(prefix):
        if not key.endswith("/meta.json"):
            continue
        raw = store.get_text(key)
        if raw:
            metas.append(ChatMeta.model_validate_json(raw))
    metas.sort(key=lambda item: item.updated_at, reverse=True)
    return metas
