"""Run one chat turn when Lambda invokes this process over HTTP."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from api.require_access_token import ChatCaller, require_access_token
from model.chat.research_job import ResearchJob
from pipeline.run_chat_turn import run_chat_turn

router = APIRouter()


@router.post("/internal/research")
def run_research(
    body: ResearchJob,
    caller: ChatCaller = Depends(require_access_token),
) -> dict[str, bool]:
    """Finish the turn. Not registered on API Gateway; only a direct invoke hits it."""
    run_chat_turn(
        body.chat_id,
        body.run_id,
        body.brief,
        access_token=caller.token,
    )
    return {"ok": True}
