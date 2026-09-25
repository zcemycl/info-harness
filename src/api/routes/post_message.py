"""Accept a prompt, store it, and start research."""

from __future__ import annotations

from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException

from api.require_access_token import require_access_token
from api.start_research import start_research
from model.chat.chat_message import ChatMessage
from model.chat.prompt_body import PromptBody
from tools.chat.append_message import append_message
from tools.chat.build_turn_brief import build_turn_brief
from tools.chat.load_history import load_history
from tools.chat.put_run_status import put_run_status

router = APIRouter()


@router.post("/chats/{chat_id}/messages")
def post_message(
    chat_id: str,
    body: PromptBody,
    access_token: str = Depends(require_access_token),
) -> dict[str, str]:
    """Append the user turn and start PEWE with last-answer context."""
    history = load_history(chat_id)
    if history is None:
        raise HTTPException(status_code=404, detail="chat not found")
    last_answer = _last_assistant(history)
    saved = append_message(chat_id, role="user", content=body.prompt.strip())
    if saved is None:
        raise HTTPException(status_code=404, detail="chat not found")
    brief = build_turn_brief(last_answer=last_answer, prompt=body.prompt)
    run_id = uuid4().hex[:12]
    put_run_status(chat_id, run_id, "running", brief=brief)
    try:
        start_research(chat_id, run_id, brief, access_token=access_token)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    return {"chat_id": chat_id, "run_id": run_id}


def _last_assistant(history: list[ChatMessage]) -> str | None:
    for message in reversed(history):
        if message.role == "assistant" and message.content.strip():
            return message.content
    return None
