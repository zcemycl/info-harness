"""Structured planner response for the FDA label specialist loop."""

from __future__ import annotations

from pydantic import BaseModel, Field

from model.research.worker_plan import WorkerPlan


class PlannerOutput(BaseModel):
    """Planner turn: rationale plus zero or more worker tasks."""

    rationale: str = Field(description="Why these tasks address the brief")
    tasks: list[WorkerPlan] = Field(
        default_factory=list,
        description="Worker tasks to run this loop (empty if nothing to do)",
    )
