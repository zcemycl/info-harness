"""Planner output: which CTG worker to run and which sections to fetch."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field, model_validator

from model.ctg.ctg_attr_name import CtgAttrName


class CtgWorkerName(StrEnum):
    """Fixed CTG workers the specialist may dispatch."""

    NCTID = "nctid"
    CONDITION = "condition"


class CtgWorkerPlan(BaseModel):
    """One executor task for a single CTG worker."""

    worker: CtgWorkerName = Field(
        description=(
            "Search axis: 'nctid' for a known NCT######## id; "
            "'condition' to autocomplete CTG condition name strings. "
            "Never invent NCT IDs."
        )
    )
    query: str = Field(
        description=(
            "Exact query for that axis: NCT######## if worker=nctid; "
            "condition phrase if worker=condition."
        )
    )
    attrs: list[CtgAttrName] = Field(
        default_factory=list,
        description=(
            "CtgByNctidRow sections for worker=nctid (required, min 1). "
            "Ignored for worker=condition. Values: basic_info, demographics, "
            "conditions, locations, adverse_events, outcomes."
        ),
    )
    both_sides: bool = Field(
        default=False,
        description=(
            "worker=condition only: false → SQL LIKE q% (prefix); "
            "true → SQL LIKE %q% (substring either side). Ignored for nctid."
        ),
    )
    offset: int = Field(default=0, ge=0, description="Pagination offset (nctid)")
    limit: int = Field(default=5, ge=1, le=20, description="Page size (nctid)")

    @model_validator(mode="after")
    def _require_attrs_for_nctid(self) -> CtgWorkerPlan:
        if self.worker is CtgWorkerName.NCTID and not self.attrs:
            raise ValueError("worker=nctid requires at least one attr")
        return self
