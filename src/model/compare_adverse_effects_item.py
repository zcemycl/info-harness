"""Request body for FDA adverse-effects compare."""

from __future__ import annotations

from pydantic import BaseModel, Field


class CompareAdverseEffectsItem(BaseModel):
    """Setids to compare for adverse-effects matrices (hc-backend Item)."""

    setids: list[str] = Field(
        min_length=1,
        description="SPL setids whose AE tables should be compared",
    )
