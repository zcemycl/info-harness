"""One turn stored in chat history."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


class ChatMessage(BaseModel):
    """User or assistant message persisted on S3 or local disk."""

    role: Literal["user", "assistant"]
    content: str
    ts: str
    run_id: str | None = None
