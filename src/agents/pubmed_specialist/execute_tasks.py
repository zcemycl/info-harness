"""Executor step: dispatch PubmedWorkerPlans to id-sections tools."""

from __future__ import annotations

from typing import Any

from agents.pubmed_id_sections.run_plan import run_id_sections_plan
from model.pubmed.pubmed_attr_name import PubmedAttrName
from model.pubmed.pubmed_attr_page import PubmedAttrPage
from model.pubmed.pubmed_worker_plan import PubmedWorkerName, PubmedWorkerPlan
from tools.trace_call import trace_info, trace_span

IdTriple = tuple[PubmedWorkerPlan, PubmedAttrName, PubmedAttrPage[Any]]


def execute_pubmed_tasks(
    tasks: list[PubmedWorkerPlan],
) -> tuple[list[IdTriple], list[str]]:
    """Run each plan via pubmed_id_sections; return triples + failures."""
    triples: list[IdTriple] = []
    failures: list[str] = []
    for plan in tasks:
        if plan.worker is not PubmedWorkerName.ID:
            failures.append(f"Unsupported worker: {plan.worker}")
            continue
        for attr in plan.attrs:
            with trace_span(
                "worker",
                "id",
                query=plan.query,
                attr=attr.value,
                offset=plan.offset,
                limit=plan.limit,
            ):
                single = plan.model_copy(update={"attrs": [attr]})
                try:
                    pages = run_id_sections_plan(single)
                except (RuntimeError, ValueError) as exc:
                    msg = f"worker=id query={plan.query!r} " f"attr={attr.value}: {exc}"
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
