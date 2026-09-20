"""Execute a WorkerPlan against indication attribute tools (no LLM)."""

from __future__ import annotations

from typing import Any

from model.fda.fda_label_attr_page import FdaLabelAttrPage
from model.research.worker_plan import WorkerPlan
from tools.fda.search_fdalabel_indication.attr_registry import INDICATION_ATTR_SEARCH


def run_indication_plan(plan: WorkerPlan) -> list[FdaLabelAttrPage[Any]]:
    """Call fixed indication attr tools for each attr on the plan."""
    pages: list[FdaLabelAttrPage[Any]] = []
    for attr in plan.attrs:
        search = INDICATION_ATTR_SEARCH.get(attr)
        if search is None:
            raise ValueError(f"Unsupported indication attr: {attr}")
        pages.append(
            search(
                plan.query,
                offset=plan.offset,
                limit=plan.limit,
                maxn=plan.maxn,
            )
        )
    return pages
