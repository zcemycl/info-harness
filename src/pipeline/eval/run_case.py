"""Run one eval case (worker or inner) and score fixtures + optional judge."""

from __future__ import annotations

from model.eval.eval_case_report import EvalCaseReport
from model.eval.eval_layer import EvalLayer
from model.eval.inner_eval_case import InnerEvalCase
from model.eval.worker_eval_case import WorkerEvalCase
from pipeline.eval.load_case import load_eval_case
from pipeline.eval.run_worker_case import run_worker_eval_case
from pipeline.eval.score_fixtures import score_inner_fixtures, score_worker_fixtures
from pipeline.eval.score_llm_judge import (
    resolve_pass_threshold,
    score_inner_judge,
    score_worker_judge,
)
from pipeline.run_fda_label_specialist import run_fda_label_specialist_pipeline


def run_eval_case(
    layer: EvalLayer,
    case_id: str,
    *,
    use_judge: bool = True,
    run_id: str | None = None,
) -> EvalCaseReport:
    """Load case, run agent(s), score fixtures and optionally LLM judge."""
    case = load_eval_case(layer, case_id)
    if isinstance(case, WorkerEvalCase):
        return _run_worker(case, use_judge=use_judge, run_id=run_id)
    return _run_inner(case, use_judge=use_judge, run_id=run_id)


def _run_worker(
    case: WorkerEvalCase, *, use_judge: bool, run_id: str | None
) -> EvalCaseReport:
    answer = run_worker_eval_case(case, run_id=run_id)
    fixtures = score_worker_fixtures(case, answer)
    threshold = resolve_pass_threshold(case.pass_threshold)
    judge = None
    if use_judge:
        judge = score_worker_judge(
            brief=case.brief, answer=answer, pass_threshold=threshold
        )
    passed = fixtures.passed and (judge.passed if judge else True)
    return EvalCaseReport(
        case_id=case.id,
        layer=EvalLayer.WORKER,
        brief=case.brief,
        passed=passed,
        fixtures=fixtures,
        judge=judge,
        run_id=answer.run_id,
        answer_preview=answer.answer[:400],
        extras={"tools_called": answer.extras.get("tools_called") or []},
    )


def _run_inner(
    case: InnerEvalCase, *, use_judge: bool, run_id: str | None
) -> EvalCaseReport:
    rid = run_id or f"eval-i-{case.id}"
    result = run_fda_label_specialist_pipeline(
        case.brief, max_loops=case.max_loops, run_id=rid
    )
    fixtures = score_inner_fixtures(case, result)
    threshold = resolve_pass_threshold(case.pass_threshold)
    judge = None
    if use_judge:
        judge = score_inner_judge(
            brief=case.brief, result=result, pass_threshold=threshold
        )
    passed = fixtures.passed and (judge.passed if judge else True)
    return EvalCaseReport(
        case_id=case.id,
        layer=EvalLayer.INNER,
        brief=case.brief,
        passed=passed,
        fixtures=fixtures,
        judge=judge,
        run_id=result.answer.run_id,
        answer_preview=result.answer.answer[:400],
        extras={
            "loops": result.loops,
            "evidence": len(result.evidence),
            "diary_decisions": [d.decision.value for d in result.diary],
        },
    )
