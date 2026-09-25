"""Poll run events after a sequence cursor."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from api.require_access_token import ChatCaller, require_access_token
from model.chat.run_event import RunEvent
from tools.chat.bind_chat_owner import bind_chat_owner
from tools.chat.load_run import load_run
from tools.chat.load_run_events import load_run_events

router = APIRouter()


@router.get("/runs/{run_id}/events", response_model=list[RunEvent])
def get_events(
    run_id: str,
    after: int = 0,
    caller: ChatCaller = Depends(require_access_token),
) -> list[RunEvent]:
    """Return this user's events with ``seq`` greater than ``after``."""
    with bind_chat_owner(caller.sub):
        if load_run(run_id) is None:
            raise HTTPException(status_code=404, detail="run not found")
        return [event for event in load_run_events(run_id) if event.seq > after]
