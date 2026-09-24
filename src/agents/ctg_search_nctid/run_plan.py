"""Execute a CtgWorkerPlan against NCT-id attribute tools (no LLM)."""

from __future__ import annotations

from typing import Any

from model.ctg.ctg_attr_page import CtgAttrPage
from model.ctg.ctg_worker_plan import CtgWorkerPlan
from tools.ctg.search_ctg_nctid.attr_registry import NCTID_ATTR_SEARCH


def run_nctid_plan(plan: CtgWorkerPlan) -> list[CtgAttrPage[Any]]:
    """Call fixed NCT-id section tools for each attr on the plan."""
    pages: list[CtgAttrPage[Any]] = []
    for attr in plan.attrs:
        search = NCTID_ATTR_SEARCH.get(attr)
        if search is None:
            raise ValueError(f"Unsupported nctid attr: {attr}")
        pages.append(
            search(
                plan.query,
                offset=plan.offset,
                limit=plan.limit,
            )
        )
    return pages
