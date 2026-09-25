"""POST body for an async research invocation."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ResearchJob(BaseModel):
    """Identifiers the worker needs to finish one chat turn."""

    chat_id: str = Field(min_length=1)
    run_id: str = Field(min_length=1)
    brief: str = Field(min_length=1)
