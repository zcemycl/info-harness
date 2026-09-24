"""Inner-loop (FDA specialist) eval case and nested expectations."""

from __future__ import annotations

from pydantic import BaseModel, Field

from model.fda.fda_attr_name import FdaAttrName
from model.research.worker_plan import FdaWorkerName


class PlannerExpectations(BaseModel):
    """Fixture checks against the first planner stage."""

    allowed_workers: list[FdaWorkerName] = Field(default_factory=list)
    required_workers: list[FdaWorkerName] = Field(default_factory=list)
    required_attrs: list[FdaAttrName] = Field(default_factory=list)


class FinalExpectations(BaseModel):
    """Fixture checks against the synthesized specialist answer."""

    status_in: list[str] = Field(default_factory=lambda: ["ok"])
    must_include: list[str] = Field(default_factory=list)
    must_not_include: list[str] = Field(default_factory=list)


class InnerEvalCase(BaseModel):
    """One FDA label specialist (inner PEWE) benchmark case."""

    id: str
    brief: str
    tags: list[str] = Field(default_factory=list)
    source_run_id: str | None = None
    pass_threshold: float | None = None
    max_loops: int | None = Field(default=None, ge=1)
    planner: PlannerExpectations = Field(default_factory=PlannerExpectations)
    evidence_min_count: int = Field(default=1, ge=0)
    final: FinalExpectations = Field(default_factory=FinalExpectations)
    must_reach_complete: bool = True
