"""Delete a chat session."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Response

from tools.chat.delete_chat import delete_chat as delete_chat_record

router = APIRouter()


@router.delete("/chats/{chat_id}", status_code=204)
def delete_chat(chat_id: str) -> Response:
    """Remove the conversation and its run files."""
    if not delete_chat_record(chat_id):
        raise HTTPException(status_code=404, detail="chat not found")
    return Response(status_code=204)
