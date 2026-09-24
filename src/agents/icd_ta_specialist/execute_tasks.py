"""Executor step: dispatch IcdWorkerPlans to search_therapeutic_area."""

from __future__ import annotations

from agents.icd_ta_worker.run_plan import run_icd_ta_plan
from model.therapeutic_area.icd_worker_plan import IcdWorkerPlan
from tools.trace_call import trace_info, trace_span


def execute_icd_tasks(
    tasks: list[IcdWorkerPlan],
) -> tuple[list[tuple[IcdWorkerPlan, list[str]]], list[str]]:
    """Run each plan; return (plan, names) pairs + failures."""
    pairs: list[tuple[IcdWorkerPlan, list[str]]] = []
    failures: list[str] = []
    for plan in tasks:
        like = "%q%" if plan.both_sides else "q%"
        with trace_span(
            "worker",
            "icd_ta",
            q=plan.q,
            both_sides=plan.both_sides,
            like=like,
        ):
            try:
                names = run_icd_ta_plan(plan)
            except (RuntimeError, ValueError) as exc:
                msg = f"q={plan.q!r} both_sides={plan.both_sides}: {exc}"
                failures.append(msg)
                trace_info("search failed", error=str(exc))
                continue
            trace_info("hits", count=len(names))
            if not names:
                failures.append(
                    f"q={plan.q!r} both_sides={plan.both_sides} ({like}): empty"
                )
            pairs.append((plan, names))
    return pairs, failures
