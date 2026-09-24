"""Executor step: dispatch WorkerPlans to axis workers."""

from __future__ import annotations

from typing import Any

from agents.fda_search_id.run_plan import run_id_plan
from agents.fda_search_indication.run_plan import run_indication_plan
from agents.fda_search_therapeutic_area.run_plan import run_therapeutic_area_plan
from agents.fda_search_tradename.run_plan import run_tradename_plan
from model.fda.fda_label_attr_page import FdaLabelAttrPage
from model.research.worker_plan import FdaAttrName, FdaWorkerName, WorkerPlan
from tools.trace_call import trace_info, trace_span


def execute_fda_tasks(
    tasks: list[WorkerPlan],
) -> tuple[
    list[tuple[WorkerPlan, FdaAttrName, FdaLabelAttrPage[Any]]],
    list[str],
]:
    """Run each plan attr via the matching worker; return triples + failures."""
    triples: list[tuple[WorkerPlan, FdaAttrName, FdaLabelAttrPage[Any]]] = []
    failures: list[str] = []
    for plan in tasks:
        for attr in plan.attrs:
            with trace_span(
                "worker",
                plan.worker.value,
                query=plan.query,
                attr=attr.value,
                offset=plan.offset,
                limit=plan.limit,
            ):
                single = plan.model_copy(update={"attrs": [attr]})
                try:
                    pages = _run_worker(single)
                except (RuntimeError, ValueError) as exc:
                    msg = (
                        f"worker={plan.worker.value} query={plan.query!r} "
                        f"attr={attr.value}: {exc}"
                    )
                    failures.append(msg)
                    trace_info("worker failed", error=str(exc))
                    continue
                for page in pages:
                    trace_info(
                        "page",
                        items=len(page.items),
                        next_offset=page.next_offset,
                    )
                    triples.append((plan, attr, page))
    return triples, failures


def _run_worker(plan: WorkerPlan) -> list[FdaLabelAttrPage[Any]]:
    if plan.worker is FdaWorkerName.TRADENAME:
        return run_tradename_plan(plan)
    if plan.worker is FdaWorkerName.INDICATION:
        return run_indication_plan(plan)
    if plan.worker is FdaWorkerName.ID:
        return run_id_plan(plan)
    if plan.worker is FdaWorkerName.THERAPEUTIC_AREA:
        return run_therapeutic_area_plan(plan)
    raise ValueError(f"Unsupported worker: {plan.worker}")
