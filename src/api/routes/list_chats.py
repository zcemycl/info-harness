"""List chats."""

from __future__ import annotations

from fastapi import APIRouter

from model.chat.chat_meta import ChatMeta
from tools.chat.list_chats import list_chats as list_chat_records

router = APIRouter()


@router.get("/chats", response_model=list[ChatMeta])
def list_chats() -> list[ChatMeta]:
    """Return conversation metadata."""
    return list_chat_records()
