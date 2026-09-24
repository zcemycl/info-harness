"""Orchestrator brief for one research workstream spawn."""

from __future__ import annotations

from pydantic import BaseModel, Field

from model.research.specialist_kind import SpecialistKind


class SpecialistBrief(BaseModel):
    """One workstream: which specialist to run and what to ask it."""

    specialist: SpecialistKind = Field(description="Which specialist pipeline to spawn")
    focus: str = Field(description="Concrete brief passed to the specialist")
    seed_queries: list[str] = Field(
        default_factory=list,
        description="Optional hints (tradename, NCT, TA phrase) for the specialist",
    )
    workstream_id: str | None = Field(
        default=None,
        description="Stable id for lock/merge; auto-assigned when omitted",
    )
