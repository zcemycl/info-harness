"""Poll run events after a sequence cursor."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from model.chat.run_event import RunEvent
from tools.chat.load_run import load_run
from tools.chat.load_run_events import load_run_events

router = APIRouter()


@router.get("/runs/{run_id}/events", response_model=list[RunEvent])
def get_events(run_id: str, after: int = 0) -> list[RunEvent]:
    """Return events with ``seq`` greater than ``after``."""
    if load_run(run_id) is None:
        raise HTTPException(status_code=404, detail="run not found")
    return [event for event in load_run_events(run_id) if event.seq > after]
