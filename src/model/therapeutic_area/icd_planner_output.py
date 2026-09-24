"""Planner output for the ICD therapeutic-area specialist."""

from __future__ import annotations

from pydantic import BaseModel, Field

from model.therapeutic_area.icd_worker_plan import IcdWorkerPlan


class IcdPlannerOutput(BaseModel):
    """Planner turn: rationale plus zero or more ICD TA searches."""

    rationale: str = Field(description="Why these searches address the brief")
    tasks: list[IcdWorkerPlan] = Field(
        default_factory=list,
        description="search_therapeutic_area tasks (empty if nothing to do)",
    )
