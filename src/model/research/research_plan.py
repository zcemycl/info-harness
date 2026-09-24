"""Outer research planner output: multi-workstream plan."""

from __future__ import annotations

from pydantic import BaseModel, Field

from model.research.specialist_brief import SpecialistBrief


class ResearchPlan(BaseModel):
    """Planner output for one research outer loop."""

    rationale: str = Field(description="Why these workstreams were chosen")
    general_directions: list[str] = Field(
        default_factory=list,
        description="Cross-cutting strategy notes for this and later loops",
    )
    selected: list[SpecialistBrief] = Field(
        default_factory=list,
        description="Workstreams to spawn this loop",
    )
