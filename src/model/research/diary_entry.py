"""Append-only outer/worker loop diary entry."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field


class DiaryDecision(StrEnum):
    """Evaluator decision carried into the next planner pass."""

    CONTINUE = "continue"
    REPLAN = "replan"
    COMPLETE = "complete"


class DiaryEntry(BaseModel):
    """Structured feedback for the next Planner (not the evidence ledger)."""

    loop: int = Field(..., ge=1, description="Outer or worker loop index")
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
