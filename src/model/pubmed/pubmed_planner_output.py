"""Structured planner response for the PubMed specialist loop."""

from __future__ import annotations

from pydantic import BaseModel, Field

from model.pubmed.pubmed_worker_plan import PubmedWorkerPlan


class PubmedPlannerOutput(BaseModel):
    """Planner turn: rationale plus zero or more PubMed worker tasks."""

    rationale: str = Field(description="Why these tasks address the brief")
    tasks: list[PubmedWorkerPlan] = Field(
        default_factory=list,
        description="Worker tasks to run this loop (empty if nothing to do)",
    )
