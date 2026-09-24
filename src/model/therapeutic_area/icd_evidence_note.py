"""Evidence note from an ICD therapeutic-area search."""

from __future__ import annotations

from pydantic import BaseModel, Field


class IcdEvidenceNote(BaseModel):
    """One compressed ledger row from search_therapeutic_area results."""

    query: str = Field(description="q passed to search_therapeutic_area")
    both_sides: bool = Field(
        description="false=q% prefix; true=%q% either-side substring"
    )
    names: list[str] = Field(
        default_factory=list,
        description="Matching therapeutic area names from the API",
    )
    summary: str = Field(description="Short text for the evaluator")
