"""Execute a CtgWorkerPlan against resolve_trial_mention (no LLM)."""

from __future__ import annotations

from model.ctg.ctg_worker_plan import CtgWorkerPlan
from model.ctg.resolved_trial import ResolvedTrial
from tools.ctg.resolve_trial_mention import resolve_trial_mention


def run_resolve_trial_plan(plan: CtgWorkerPlan) -> ResolvedTrial:
    """Call resolve_trial_mention for one plan."""
    return resolve_trial_mention(plan.query, page_size=plan.limit)
