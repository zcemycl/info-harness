"""Execute a CtgWorkerPlan against live NCT-id fetch tools (no LLM)."""

from __future__ import annotations

from typing import Any

from model.ctg.ctg_attr_page import CtgAttrPage
from model.ctg.ctg_worker_plan import CtgWorkerPlan
from tools.ctg.fetch_ctg_nctid.attr_registry import NCTID_ATTR_FETCH


def run_fetch_plan(plan: CtgWorkerPlan) -> list[CtgAttrPage[Any]]:
    """Call fixed live NCT-id section tools for each attr on the plan."""
    pages: list[CtgAttrPage[Any]] = []
    for attr in plan.attrs:
        fetch = NCTID_ATTR_FETCH.get(attr)
        if fetch is None:
            raise ValueError(f"Unsupported fetch attr: {attr}")
        pages.append(
            fetch(
                plan.query,
                offset=plan.offset,
                limit=plan.limit,
            )
        )
    return pages
