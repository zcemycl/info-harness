"""Structured planner response for the CTG specialist loop."""

from __future__ import annotations

from pydantic import BaseModel, Field

from model.ctg.ctg_worker_plan import CtgWorkerPlan


class CtgPlannerOutput(BaseModel):
    """Planner turn: rationale plus zero or more CTG worker tasks."""

    rationale: str = Field(description="Why these tasks address the brief")
    tasks: list[CtgWorkerPlan] = Field(
        default_factory=list,
        description="Worker tasks to run this loop (empty if nothing to do)",
    )
