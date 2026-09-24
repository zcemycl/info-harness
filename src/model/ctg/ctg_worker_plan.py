"""Planner output: which CTG worker to run and which sections to fetch."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field, model_validator

from model.ctg.ctg_attr_name import (
    FETCH_CTG_ATTRS,
    HC_CTG_ATTRS,
    CtgAttrName,
)


class CtgWorkerName(StrEnum):
    """Fixed CTG workers the specialist may dispatch."""

    NCTID = "nctid"
    FETCH = "fetch"
    CONDITION = "condition"
    RESOLVE_TRIAL = "resolve_trial"


class CtgWorkerPlan(BaseModel):
    """One executor task for a single CTG worker."""

    worker: CtgWorkerName = Field(
        description=(
            "Search axis: 'nctid' for HC-stored sections by NCT########; "
            "'fetch' for live ClinicalTrials.gov by NCT######## (freshest "
            "data + references); 'condition' to autocomplete CTG condition "
            "name strings; 'resolve_trial' to map study name/protocol id → "
            "NCT via CT.gov + PubMed. Never invent NCT IDs."
        )
    )
    query: str = Field(
        description=(
            "Exact query for that axis: NCT######## if worker=nctid or "
            "fetch; condition phrase if worker=condition; study name / "
            "acronym / sponsor protocol id if worker=resolve_trial."
        )
    )
    attrs: list[CtgAttrName] = Field(
        default_factory=list,
        description=(
            "Study sections for worker=nctid or fetch (required, min 1). "
            "nctid: basic_info, demographics, conditions, locations, "
            "adverse_events, outcomes. fetch: same plus references. "
            "Ignored for worker=condition and resolve_trial."
        ),
    )
    both_sides: bool = Field(
        default=False,
        description=(
            "worker=condition only: false → SQL LIKE q% (prefix); "
            "true → SQL LIKE %q% (substring either side). Ignored for "
            "nctid, fetch, and resolve_trial."
        ),
    )
    offset: int = Field(default=0, ge=0, description="Pagination offset (nctid/fetch)")
    limit: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Page size (nctid / fetch / resolve_trial)",
    )

    @model_validator(mode="after")
    def _validate_attrs_by_worker(self) -> CtgWorkerPlan:
        if self.worker is CtgWorkerName.NCTID:
            if not self.attrs:
                raise ValueError("worker=nctid requires at least one attr")
            bad = [a for a in self.attrs if a not in HC_CTG_ATTRS]
            if bad:
                names = ", ".join(a.value for a in bad)
                raise ValueError(f"worker=nctid does not support attr(s): {names}")
        elif self.worker is CtgWorkerName.FETCH:
            if not self.attrs:
                raise ValueError("worker=fetch requires at least one attr")
            bad = [a for a in self.attrs if a not in FETCH_CTG_ATTRS]
            if bad:
                names = ", ".join(a.value for a in bad)
                raise ValueError(f"worker=fetch does not support attr(s): {names}")
        return self
