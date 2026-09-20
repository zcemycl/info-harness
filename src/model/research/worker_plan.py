"""Planner output: which FDA axis worker to run and which attrs to fetch."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field

from model.fda.fda_attr_name import FdaAttrName


class FdaWorkerName(StrEnum):
    """Fixed FDA search-axis workers the specialist may dispatch."""

    TRADENAME = "tradename"
    INDICATION = "indication"


class WorkerPlan(BaseModel):
    """One executor task for a single axis worker."""

    worker: FdaWorkerName = Field(
        description=(
            "Search axis: 'tradename' for drug brand names only "
            "(Keytruda, Opdivo); 'indication' for disease/condition "
            "phrases only (HIV, melanoma). Never put a disease on tradename."
        )
    )
    query: str = Field(
        description=(
            "Exact query for that axis: brand name if worker=tradename; "
            "disease/condition if worker=indication. Example bad: "
            "worker=tradename query=HIV."
        )
    )
    attrs: list[FdaAttrName] = Field(
        min_length=1,
        description=(
            "FdaLabel section tools to return (fixed enum). Not the search axis. "
            "Values: indication, indication_usages, dosage_administrations, "
            "dosage_forms, contraindications, warning_precautions, "
            "adverse_effects, adverse_effect_tables, drug_interactions, "
            "clinical_pharmacologies, clinical_trials, clinical_trial_tables, "
            "supply_store_handles, therapeutic_areas, companies."
        ),
    )
    offset: int = Field(default=0, ge=0, description="Pagination offset")
    limit: int = Field(default=5, ge=1, le=20, description="Page size")
    maxn: int = Field(default=30, ge=1, description="Max candidates upstream")


# Re-export for existing imports of FdaAttrName from worker_plan.
__all__ = ["FdaWorkerName", "FdaAttrName", "WorkerPlan"]
