"""Dispatch a worker eval case to the matching FDA / CTG axis runner."""

from __future__ import annotations

from agents.ctg_resolve_trial.run import run_ctg_resolve_trial
from agents.ctg_search_condition.run import run_ctg_search_condition
from agents.ctg_search_nctid.run import run_ctg_search_nctid
from agents.fda_search_id.run import run_fda_search_id
from agents.fda_search_indication.run import run_fda_search_indication
from agents.fda_search_therapeutic_area.run import run_fda_search_therapeutic_area
from agents.fda_search_tradename.run import run_fda_search_tradename
from model.eval.eval_worker_name import EvalWorkerName
from model.eval.worker_eval_case import WorkerEvalCase
from model.research.agent_answer import AgentAnswer


def run_worker_eval_case(
    case: WorkerEvalCase, *, run_id: str | None = None
) -> AgentAnswer:
    """Execute the worker named in the case against its brief."""
    rid = run_id or f"eval-w-{case.id}"
    if case.worker is EvalWorkerName.TRADENAME:
        return run_fda_search_tradename(case.brief, run_id=rid)
    if case.worker is EvalWorkerName.INDICATION:
        return run_fda_search_indication(case.brief, run_id=rid)
    if case.worker is EvalWorkerName.ID:
        return run_fda_search_id(case.brief, run_id=rid)
    if case.worker is EvalWorkerName.THERAPEUTIC_AREA:
        return run_fda_search_therapeutic_area(case.brief, run_id=rid)
    if case.worker is EvalWorkerName.NCTID:
        return run_ctg_search_nctid(case.brief, run_id=rid)
    if case.worker is EvalWorkerName.CONDITION:
        return run_ctg_search_condition(case.brief, run_id=rid)
    if case.worker is EvalWorkerName.RESOLVE_TRIAL:
        return run_ctg_resolve_trial(case.brief, run_id=rid)
    raise ValueError(f"Unknown worker: {case.worker}")
