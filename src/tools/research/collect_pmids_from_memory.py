"""Collect PMIDs already known from research memory lessons/gaps."""

from __future__ import annotations

from model.research.research_memory import ResearchMemory
from tools.research.collect_pmids import collect_pmids


def collect_pmids_from_memory(memory: ResearchMemory) -> list[str]:
    """Scan memory lessons, gaps, and settled summaries for PMIDs."""
    texts: list[str | None] = [
        *memory.lessons,
        *memory.open_gaps,
        *[s.answer_summary for s in memory.settled],
        *[t.summary for t in memory.tried_ideas],
    ]
    return collect_pmids(*texts)
