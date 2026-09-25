"""One streamed PEWE status line for a chat run."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


class RunEvent(BaseModel):
    """Stage, final answer, or error pushed to the app."""

    seq: int = 0
    ts: str
    type: Literal["stage", "final", "error"]
    run_id: str
    chat_id: str
    loop: int | None = None
    tier: Literal["outer", "inner", "worker"] | None = None
    domain: str | None = None
    stage: str | None = None
    agent: str | None = None
    status: str | None = None
    summary: str = ""
    answer: str | None = None
    path: str | None = None
    phase: Literal["start", "end"] | None = None
