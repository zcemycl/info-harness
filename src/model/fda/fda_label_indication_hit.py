"""Slim FDA label hit carrying only the indication summary."""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field


class FdaLabelIndicationHit(BaseModel):
    """Paginated search hit: ids + indication text only."""

    id: int = Field(description="Internal FDA label row id")
    setid: UUID = Field(description="SPL setid UUID")
    tradename: str = Field(description="Drug trade name")
    indication: str | None = Field(
        default=None, description="Primary indication text summary"
    )
