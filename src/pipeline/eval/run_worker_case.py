"""Dispatch a worker eval case to the matching FDA axis runner."""

from __future__ import annotations

from agents.fda_search_id.run import run_fda_search_id
from agents.fda_search_indication.run import run_fda_search_indication
from agents.fda_search_therapeutic_area.run import run_fda_search_therapeutic_area
from agents.fda_search_tradename.run import run_fda_search_tradename
from model.eval.worker_eval_case import WorkerEvalCase
from model.research.agent_answer import AgentAnswer
from model.research.worker_plan import FdaWorkerName


def run_worker_eval_case(
    case: WorkerEvalCase, *, run_id: str | None = None
) -> AgentAnswer:
    """Execute the worker named in the case against its brief."""
    rid = run_id or f"eval-w-{case.id}"
    if case.worker is FdaWorkerName.TRADENAME:
        return run_fda_search_tradename(case.brief, run_id=rid)
    if case.worker is FdaWorkerName.INDICATION:
        return run_fda_search_indication(case.brief, run_id=rid)
    if case.worker is FdaWorkerName.ID:
        return run_fda_search_id(case.brief, run_id=rid)
    if case.worker is FdaWorkerName.THERAPEUTIC_AREA:
        return run_fda_search_therapeutic_area(case.brief, run_id=rid)
    raise ValueError(f"Unknown worker: {case.worker}")
