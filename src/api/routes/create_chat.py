"""Create a chat."""

from __future__ import annotations

from fastapi import APIRouter

from model.chat.chat_meta import ChatMeta
from tools.chat.create_chat import create_chat as create_chat_record

router = APIRouter()


@router.post("/chats", response_model=ChatMeta)
def create_chat() -> ChatMeta:
    """Create an empty conversation."""
    return create_chat_record()
