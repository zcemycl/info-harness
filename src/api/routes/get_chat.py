"""Load one chat transcript."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from model.chat.chat_message import ChatMessage
from tools.chat.load_history import load_history

router = APIRouter()


@router.get("/chats/{chat_id}", response_model=list[ChatMessage])
def get_chat(chat_id: str) -> list[ChatMessage]:
    """Return messages for ``chat_id``."""
    history = load_history(chat_id)
    if history is None:
        raise HTTPException(status_code=404, detail="chat not found")
    return history
