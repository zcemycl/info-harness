"""Create a chat."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from api.require_access_token import ChatCaller, require_access_token
from model.chat.chat_meta import ChatMeta
from tools.chat.bind_chat_owner import bind_chat_owner
from tools.chat.create_chat import create_chat as create_chat_record

router = APIRouter()


@router.post("/chats", response_model=ChatMeta)
def create_chat(caller: ChatCaller = Depends(require_access_token)) -> ChatMeta:
    """Create an empty conversation for the signed-in user."""
    with bind_chat_owner(caller.sub):
        return create_chat_record()
