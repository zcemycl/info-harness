"""Status plus final answer for one research run."""

from __future__ import annotations

from pydantic import BaseModel


class RunView(BaseModel):
    """What ``GET /runs/{run_id}`` returns."""

    chat_id: str
    run_id: str
    status: str
    brief: str = ""
    answer: str | None = None
    error: str | None = None
    loops: int | None = None
