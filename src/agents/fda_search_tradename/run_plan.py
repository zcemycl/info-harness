"""Execute a WorkerPlan against tradename attribute tools (no LLM)."""

from __future__ import annotations

from typing import Any

from model.fda.fda_label_attr_page import FdaLabelAttrPage
from model.research.worker_plan import FdaAttrName, WorkerPlan
from tools.fda.search_fdalabel_tradename.adverse_effects import (
    search_fdalabel_tradename_adverse_effects,
)
from tools.fda.search_fdalabel_tradename.indication import (
    search_fdalabel_tradename_indication,
)


def run_tradename_plan(plan: WorkerPlan) -> list[FdaLabelAttrPage[Any]]:
    """Call fixed tradename attr tools for each attr on the plan."""
    pages: list[FdaLabelAttrPage[Any]] = []
    for attr in plan.attrs:
        if attr is FdaAttrName.INDICATION:
            pages.append(
                search_fdalabel_tradename_indication(
                    plan.query,
                    offset=plan.offset,
                    limit=plan.limit,
                    maxn=plan.maxn,
                )
            )
        elif attr is FdaAttrName.ADVERSE_EFFECTS:
            pages.append(
                search_fdalabel_tradename_adverse_effects(
                    plan.query,
                    offset=plan.offset,
                    limit=plan.limit,
                    maxn=plan.maxn,
                )
            )
        else:
            raise ValueError(f"Unsupported tradename attr: {attr}")
    return pages
