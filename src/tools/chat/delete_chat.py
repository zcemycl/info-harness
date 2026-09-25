"""Delete one chat and its run index entries."""

from __future__ import annotations

import json
import shutil

from tools.chat.bind_chat_owner import current_chat_owner
from tools.chat.object_key import object_key
from tools.chat.object_store import open_object_store


def delete_chat(chat_id: str) -> bool:
    """Remove the chat tree. Return ``False`` when it does not exist."""
    store = open_object_store()
    owner = current_chat_owner()
    if store.get_text(object_key("meta", chat_id=chat_id)) is None:
        return False
    prefix = f"users/{owner}/chats/{chat_id}"
    for key in store.list_prefix(prefix):
        store.delete_text(key)
    run_index = f"users/{owner}/run-index"
    for key in store.list_prefix(run_index):
        raw = store.get_text(key)
        if not raw:
            continue
        if json.loads(raw).get("chat_id") == chat_id:
            store.delete_text(key)
    folder = store.root / "users" / owner / "chats" / chat_id
    if not store.bucket and folder.is_dir():
        shutil.rmtree(folder)
    return True
