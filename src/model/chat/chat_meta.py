"""Chat list metadata."""

from __future__ import annotations

from pydantic import BaseModel


class ChatMeta(BaseModel):
    """Sidebar row for one conversation."""

    chat_id: str
    title: str
    created_at: str
    updated_at: str
