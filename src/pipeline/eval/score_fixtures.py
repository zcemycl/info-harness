"""Deterministic fixture scoring for worker and inner eval cases."""

from __future__ import annotations

from model.eval.fixture_score import FixtureCheck, FixtureScore
from model.eval.inner_eval_case import InnerEvalCase
from model.eval.worker_eval_case import WorkerEvalCase
from model.research.agent_answer import AgentAnswer
from model.research.diary_entry import DiaryDecision
from model.research.fda_specialist_result import FdaSpecialistResult


def score_worker_fixtures(case: WorkerEvalCase, answer: AgentAnswer) -> FixtureScore:
    """Score a worker AgentAnswer against case fixtures."""
    checks: list[FixtureCheck] = []
    text = answer.answer or ""
    lower = text.lower()
    tools = [str(t) for t in (answer.extras.get("tools_called") or [])]

    checks.append(
        FixtureCheck(
            name="status_in",
            ok=answer.status.value in case.status_in,
            detail=f"got={answer.status.value} want={case.status_in}",
        )
    )
    checks.append(
        FixtureCheck(
            name="min_answer_chars",
            ok=len(text) >= case.min_answer_chars,
            detail=f"len={len(text)} min={case.min_answer_chars}",
        )
    )
    for needle in case.must_include:
        checks.append(
            FixtureCheck(
                name=f"must_include:{needle}",
                ok=needle.lower() in lower,
                detail="missing" if needle.lower() not in lower else "ok",
            )
        )
    for needle in case.must_not_include:
        checks.append(
            FixtureCheck(
                name=f"must_not_include:{needle}",
                ok=needle.lower() not in lower,
                detail="present" if needle.lower() in lower else "ok",
            )
        )
    if case.expected_tools_any:
        ok = any(t in tools for t in case.expected_tools_any)
        checks.append(
            FixtureCheck(
                name="expected_tools_any",
                ok=ok,
                detail=f"called={tools} any_of={case.expected_tools_any}",
            )
        )
    if case.expected_tools_all:
        missing = [t for t in case.expected_tools_all if t not in tools]
        checks.append(
            FixtureCheck(
                name="expected_tools_all",
                ok=not missing,
                detail=f"called={tools} missing={missing}",
            )
        )
    return FixtureScore(passed=all(c.ok for c in checks), checks=checks)


def score_inner_fixtures(
    case: InnerEvalCase, result: FdaSpecialistResult
) -> FixtureScore:
    """Score a specialist result against inner-case fixtures."""
    checks: list[FixtureCheck] = []
    answer = result.answer
    text = answer.answer or ""
    lower = text.lower()

    checks.append(
        FixtureCheck(
            name="final.status_in",
            ok=answer.status.value in case.final.status_in,
            detail=f"got={answer.status.value} want={case.final.status_in}",
        )
    )
    for needle in case.final.must_include:
        checks.append(
            FixtureCheck(
                name=f"final.must_include:{needle}",
                ok=needle.lower() in lower,
                detail="missing" if needle.lower() not in lower else "ok",
            )
        )
    for needle in case.final.must_not_include:
        checks.append(
            FixtureCheck(
                name=f"final.must_not_include:{needle}",
                ok=needle.lower() not in lower,
                detail="present" if needle.lower() in lower else "ok",
            )
        )
    checks.append(
        FixtureCheck(
            name="evidence_min_count",
            ok=len(result.evidence) >= case.evidence_min_count,
            detail=f"got={len(result.evidence)} min={case.evidence_min_count}",
        )
    )
    if case.must_reach_complete:
        reached = any(d.decision is DiaryDecision.COMPLETE for d in result.diary)
        checks.append(
            FixtureCheck(
                name="must_reach_complete",
                ok=reached,
                detail="no COMPLETE diary decision" if not reached else "ok",
            )
        )
    checks.extend(_planner_checks(case, result))
    return FixtureScore(passed=all(c.ok for c in checks), checks=checks)


def _planner_checks(
    case: InnerEvalCase, result: FdaSpecialistResult
) -> list[FixtureCheck]:
    planner = next((a for a in result.stage_answers if a.agent == "planner"), None)
    tasks = (planner.extras.get("tasks") if planner else None) or []
    workers = {str(t.get("worker")) for t in tasks if isinstance(t, dict)}
    attrs: set[str] = set()
    for task in tasks:
        if isinstance(task, dict):
            for attr in task.get("attrs") or []:
                attrs.add(str(attr))
    out: list[FixtureCheck] = []
    if case.planner.required_workers:
        need = {w.value for w in case.planner.required_workers}
        missing = sorted(need - workers)
        out.append(
            FixtureCheck(
                name="planner.required_workers",
                ok=not missing,
                detail=f"got={sorted(workers)} missing={missing}",
            )
        )
    if case.planner.allowed_workers:
        allow = {w.value for w in case.planner.allowed_workers}
        bad = sorted(workers - allow)
        out.append(
            FixtureCheck(
                name="planner.allowed_workers",
                ok=not bad,
                detail=f"got={sorted(workers)} disallowed={bad}",
            )
        )
    if case.planner.required_attrs:
        need_a = {a.value for a in case.planner.required_attrs}
        missing_a = sorted(need_a - attrs)
        out.append(
            FixtureCheck(
                name="planner.required_attrs",
                ok=not missing_a,
                detail=f"got={sorted(attrs)} missing={missing_a}",
            )
        )
    return out
