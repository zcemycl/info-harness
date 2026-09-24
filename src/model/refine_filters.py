"""Refine filters applied after advanced compare-filter search."""

from __future__ import annotations

from pydantic import BaseModel, Field


class RefineFilters(BaseModel):
    """Overlap / facet refine filters for FDA and CTG compare search."""

    therapeutic_area_paths: list[str] = Field(
        default_factory=list,
        description="TA ltree paths used for graph/path overlap scoring",
    )
    conditions: list[str] = Field(
        default_factory=list,
        description="Condition names for overlap scoring",
    )
    countries: list[str] = Field(
        default_factory=list,
        description="Country names for overlap scoring",
    )
    std_ages: list[str] = Field(
        default_factory=list,
        description="Standard age-group labels for overlap scoring",
    )
    phases: list[str] = Field(
        default_factory=list,
        description="CTG phase labels for overlap scoring",
    )
