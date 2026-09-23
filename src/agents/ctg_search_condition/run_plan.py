"""Execute a CtgWorkerPlan against search_ctg_condition (no LLM)."""

from __future__ import annotations

from model.ctg.ctg_worker_plan import CtgWorkerPlan
from tools.ctg.search_ctg_condition import search_ctg_condition


def run_condition_plan(plan: CtgWorkerPlan) -> list[str]:
    """Call search_ctg_condition for one plan; return matching names."""
    return search_ctg_condition(plan.query, both_sides=plan.both_sides)
