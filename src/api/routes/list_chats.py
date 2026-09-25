"""List chats."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from api.require_access_token import ChatCaller, require_access_token
from model.chat.chat_meta import ChatMeta
from tools.chat.bind_chat_owner import bind_chat_owner
from tools.chat.list_chats import list_chats as list_chat_records

router = APIRouter()


@router.get("/chats", response_model=list[ChatMeta])
def list_chats(caller: ChatCaller = Depends(require_access_token)) -> list[ChatMeta]:
    """Return this user's conversation metadata."""
    with bind_chat_owner(caller.sub):
        return list_chat_records()
