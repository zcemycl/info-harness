"""Execute a PubmedWorkerPlan against PMID section tools (no LLM)."""

from __future__ import annotations

from typing import Any

from model.pubmed.pubmed_attr_page import PubmedAttrPage
from model.pubmed.pubmed_worker_plan import PubmedWorkerPlan
from tools.pubmed.id_sections.attr_registry import ID_ATTR_SECTIONS


def run_id_sections_plan(plan: PubmedWorkerPlan) -> list[PubmedAttrPage[Any]]:
    """Call fixed PMID section tools for each attr on the plan."""
    pages: list[PubmedAttrPage[Any]] = []
    for attr in plan.attrs:
        fetch = ID_ATTR_SECTIONS.get(attr)
        if fetch is None:
            raise ValueError(f"Unsupported pubmed id attr: {attr}")
        pages.append(
            fetch(
                plan.query,
                offset=plan.offset,
                limit=plan.limit,
            )
        )
    return pages
