"""Load one chat transcript."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from api.require_access_token import ChatCaller, require_access_token
from model.chat.chat_message import ChatMessage
from tools.chat.bind_chat_owner import bind_chat_owner
from tools.chat.load_history import load_history

router = APIRouter()


@router.get("/chats/{chat_id}", response_model=list[ChatMessage])
def get_chat(
    chat_id: str,
    caller: ChatCaller = Depends(require_access_token),
) -> list[ChatMessage]:
    """Return messages for this user's ``chat_id``."""
    with bind_chat_owner(caller.sub):
        history = load_history(chat_id)
    if history is None:
        raise HTTPException(status_code=404, detail="chat not found")
    return history
