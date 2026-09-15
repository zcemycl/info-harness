"""Refine filters applied after advanced compare-filter search."""

from __future__ import annotations

from pydantic import BaseModel, Field


class RefineFilters(BaseModel):
    """Overlap / facet refine filters for compare search."""

    therapeutic_area_paths: list[str] = Field(default_factory=list)
    conditions: list[str] = Field(default_factory=list)
    countries: list[str] = Field(default_factory=list)
    std_ages: list[str] = Field(default_factory=list)
    phases: list[str] = Field(default_factory=list)
