"""Server-sent events for run stage updates."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

from api.iter_run_events import iter_run_events
from api.require_access_token import ChatCaller, require_access_token
from tools.chat.bind_chat_owner import bind_chat_owner
from tools.chat.load_run import load_run

router = APIRouter()


@router.get("/runs/{run_id}/events/stream")
def stream_events(
    run_id: str,
    after: int = 0,
    caller: ChatCaller = Depends(require_access_token),
) -> StreamingResponse:
    """Stream this user's stage lines."""
    with bind_chat_owner(caller.sub):
        if load_run(run_id) is None:
            raise HTTPException(status_code=404, detail="run not found")
    return StreamingResponse(
        iter_run_events(run_id, after, caller.sub),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )
