"""Request body for a chat follow-up."""

from __future__ import annotations

from pydantic import BaseModel, Field


class PromptBody(BaseModel):
    """Next user prompt. Combined with the last answer before research."""

    prompt: str = Field(min_length=1)
