"""Server-sent events for run stage updates."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from api.iter_run_events import iter_run_events
from tools.chat.load_run import load_run

router = APIRouter()


@router.get("/runs/{run_id}/events/stream")
def stream_events(run_id: str, after: int = 0) -> StreamingResponse:
    """Stream stage lines. Poll ``/events`` if the host buffers the body."""
    if load_run(run_id) is None:
        raise HTTPException(status_code=404, detail="run not found")
    return StreamingResponse(
        iter_run_events(run_id, after),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )
