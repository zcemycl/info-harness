"""Fetch run status and the final answer."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from api.require_access_token import ChatCaller, require_access_token
from model.chat.run_view import RunView
from tools.chat.bind_chat_owner import bind_chat_owner
from tools.chat.load_run import load_run

router = APIRouter()


@router.get("/runs/{run_id}", response_model=RunView)
def get_run(
    run_id: str,
    caller: ChatCaller = Depends(require_access_token),
) -> RunView:
    """Return this user's run. ``answer`` is set once research finishes."""
    with bind_chat_owner(caller.sub):
        view = load_run(run_id)
    if view is None:
        raise HTTPException(status_code=404, detail="run not found")
    return view
