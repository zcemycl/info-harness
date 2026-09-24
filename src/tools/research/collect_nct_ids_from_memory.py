"""Collect NCT ids remembered in research memory summaries."""

from __future__ import annotations

from model.research.research_memory import ResearchMemory
from tools.research.collect_nct_ids import collect_nct_ids


def collect_nct_ids_from_memory(memory: ResearchMemory) -> list[str]:
    """Scan settled/tried answer summaries and focuses for NCT ids."""
    texts: list[str | None] = []
    for settled in memory.settled:
        texts.append(settled.focus)
        texts.append(settled.answer_summary)
    for tried in memory.tried_ideas:
        texts.append(tried.focus)
        texts.append(tried.summary)
    texts.extend(memory.open_gaps)
    texts.extend(memory.lessons)
    return collect_nct_ids(*texts)
