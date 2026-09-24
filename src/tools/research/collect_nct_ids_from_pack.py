"""Collect NCT ids already known from a research pack."""

from __future__ import annotations

from model.research.research_pack import ResearchPack
from tools.research.collect_nct_ids import collect_nct_ids


def collect_nct_ids_from_pack(pack: ResearchPack | None) -> list[str]:
    """Scan pack focuses, seeds, and answers for NCT######## ids."""
    if pack is None or not pack.outcomes:
        return []
    texts: list[str | None] = []
    for outcome in pack.outcomes:
        texts.append(outcome.brief.focus)
        texts.extend(outcome.brief.seed_queries)
        texts.append(outcome.answer.answer)
        texts.append(outcome.error)
    return collect_nct_ids(*texts)
