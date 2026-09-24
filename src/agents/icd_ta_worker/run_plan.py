"""Execute an IcdWorkerPlan against search_therapeutic_area (no LLM)."""

from __future__ import annotations

from model.therapeutic_area.icd_worker_plan import IcdWorkerPlan
from tools.therapeutic_area.search_therapeutic_area import search_therapeutic_area


def run_icd_ta_plan(plan: IcdWorkerPlan) -> list[str]:
    """Call search_therapeutic_area for one plan; return matching names."""
    return search_therapeutic_area(plan.q, both_sides=plan.both_sides)
