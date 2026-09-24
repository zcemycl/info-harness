"""Outer research evaluator result: DiaryEntry fields + next-loop directives."""

from __future__ import annotations

from pydantic import BaseModel, Field

from model.research.diary_entry import DiaryDecision
from model.research.specialist_brief import SpecialistBrief
from model.research.specialist_kind import SpecialistKind


class ResearchEvalResult(BaseModel):
    """Evaluator gate plus structured memory hints for the next planner."""

    loop: int = Field(..., ge=1)
    observations: list[str] = Field(default_factory=list)
    successful_actions: list[str] = Field(default_factory=list)
    failures: list[str] = Field(default_factory=list)
    evidence_gaps: list[str] = Field(default_factory=list)
    contradictions: list[str] = Field(default_factory=list)
    lessons: list[str] = Field(default_factory=list)
    recommended_next_actions: list[str] = Field(default_factory=list)
    decision: DiaryDecision = Field(
        ...,
        description="continue | replan | complete",
    )
    next_specialists: list[SpecialistKind] = Field(
        default_factory=list,
        description="Specialists the next planner should prioritize",
    )
    next_briefs: list[SpecialistBrief] = Field(
        default_factory=list,
        description="Concrete briefs to force into the next plan",
    )
    force_rerun_workstream_ids: list[str] = Field(
        default_factory=list,
        description="Previously settled ids that must be re-run",
    )
    reject_directions: list[str] = Field(
        default_factory=list,
        description="General directions that should not be repeated",
    )
