"""Executor step: dispatch CtgWorkerPlans to NCT-id / condition workers."""

from __future__ import annotations

from typing import Any

from agents.ctg_search_condition.run_plan import run_condition_plan
from agents.ctg_search_nctid.run_plan import run_nctid_plan
from model.ctg.ctg_attr_name import CtgAttrName
from model.ctg.ctg_attr_page import CtgAttrPage
from model.ctg.ctg_worker_plan import CtgWorkerName, CtgWorkerPlan
from tools.trace_call import trace_info, trace_span

NctidTriple = tuple[CtgWorkerPlan, CtgAttrName, CtgAttrPage[Any]]
ConditionPair = tuple[CtgWorkerPlan, list[str]]


def execute_ctg_tasks(
    tasks: list[CtgWorkerPlan],
) -> tuple[list[NctidTriple], list[ConditionPair], list[str]]:
    """Run each plan via the matching worker; return results + failures."""
    nctid_triples: list[NctidTriple] = []
    condition_pairs: list[ConditionPair] = []
    failures: list[str] = []
    for plan in tasks:
        if plan.worker is CtgWorkerName.NCTID:
            _run_nctid(plan, nctid_triples, failures)
        elif plan.worker is CtgWorkerName.CONDITION:
            _run_condition(plan, condition_pairs, failures)
        else:
            failures.append(f"Unsupported worker: {plan.worker}")
    return nctid_triples, condition_pairs, failures


def _run_nctid(
    plan: CtgWorkerPlan,
    triples: list[NctidTriple],
    failures: list[str],
) -> None:
    for attr in plan.attrs:
        with trace_span(
            "worker",
            "nctid",
            query=plan.query,
            attr=attr.value,
            offset=plan.offset,
            limit=plan.limit,
        ):
            single = plan.model_copy(update={"attrs": [attr]})
            try:
                pages = run_nctid_plan(single)
            except (RuntimeError, ValueError) as exc:
                msg = f"worker=nctid query={plan.query!r} " f"attr={attr.value}: {exc}"
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


def _run_condition(
    plan: CtgWorkerPlan,
    pairs: list[ConditionPair],
    failures: list[str],
) -> None:
    like = "%q%" if plan.both_sides else "q%"
    with trace_span(
        "worker",
        "condition",
        q=plan.query,
        both_sides=plan.both_sides,
        like=like,
    ):
        try:
            names = run_condition_plan(plan)
        except (RuntimeError, ValueError) as exc:
            msg = f"worker=condition q={plan.query!r}: {exc}"
            failures.append(msg)
            trace_info("search failed", error=str(exc))
            return
        trace_info("hits", count=len(names))
        if not names:
            failures.append(
                f"q={plan.query!r} both_sides={plan.both_sides} ({like}): empty"
            )
        pairs.append((plan, names))
