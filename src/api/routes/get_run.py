"""Fetch run status and the final answer."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from model.chat.run_view import RunView
from tools.chat.load_run import load_run

router = APIRouter()


@router.get("/runs/{run_id}", response_model=RunView)
def get_run(run_id: str) -> RunView:
    """Return status. ``answer`` is set once research finishes."""
    view = load_run(run_id)
    if view is None:
        raise HTTPException(status_code=404, detail="run not found")
    return view
