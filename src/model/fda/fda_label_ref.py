"""Compact FDA label reference nested under Manufacturer."""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field


class FdaLabelRef(BaseModel):
    """Minimal FDA label pointer used in manufacturer payloads."""

    id: int = Field(description="Internal FDA label row id")
    tradename: str = Field(description="Drug trade name")
    setid: UUID = Field(description="SPL setid UUID")
    indication: str = Field(description="Indication summary text")
