"""Slim FDA label hit carrying adverse-effects sections only."""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field

from model.fda.fda_label_section import FdaLabelSection


class FdaLabelAdverseEffectsHit(BaseModel):
    """Paginated search hit: ids + adverse-effects sections only."""

    id: int = Field(description="Internal FDA label row id")
    setid: UUID = Field(description="SPL setid UUID")
    tradename: str = Field(description="Drug trade name")
    adverse_effects: list[FdaLabelSection] | None = Field(
        default=None, description="Section 6 adverse reactions text"
    )
