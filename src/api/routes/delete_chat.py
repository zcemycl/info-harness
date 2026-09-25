"""Delete a chat session."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Response

from api.require_access_token import ChatCaller, require_access_token
from tools.chat.bind_chat_owner import bind_chat_owner
from tools.chat.delete_chat import delete_chat as delete_chat_record

router = APIRouter()


@router.delete("/chats/{chat_id}", status_code=204)
def delete_chat(
    chat_id: str,
    caller: ChatCaller = Depends(require_access_token),
) -> Response:
    """Remove this user's conversation and its run files."""
    with bind_chat_owner(caller.sub):
        removed = delete_chat_record(chat_id)
    if not removed:
        raise HTTPException(status_code=404, detail="chat not found")
    return Response(status_code=204)
