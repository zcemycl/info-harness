"""Create an empty chat."""

from __future__ import annotations

import json
from uuid import uuid4

from model.chat.chat_meta import ChatMeta
from tools.chat.object_key import object_key
from tools.chat.object_store import open_object_store
from tools.chat.utc_now import utc_now


def create_chat() -> ChatMeta:
    """Write ``meta.json`` and an empty history. Return the new meta."""
    now = utc_now()
    meta = ChatMeta(
        chat_id=uuid4().hex[:12],
        title="New chat",
        created_at=now,
        updated_at=now,
    )
    store = open_object_store()
    store.put_text(object_key("meta", chat_id=meta.chat_id), meta.model_dump_json())
    store.put_text(
        object_key("history", chat_id=meta.chat_id),
        json.dumps({"messages": []}),
    )
    return meta
