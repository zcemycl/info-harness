"""Collect upstream PMIDs from a research pack (not pubmed self-cites)."""

from __future__ import annotations

from typing import Any

from model.research.research_pack import ResearchPack
from model.research.specialist_kind import SpecialistKind
from tools.research.collect_pmids import collect_pmids


def collect_pmids_from_pack(pack: ResearchPack | None) -> list[str]:
    """Scan non-pubmed outcomes + CTG evidence.names for real PMIDs."""
    if pack is None or not pack.outcomes:
        return []
    texts: list[str | None] = []
    names: list[str] = []
    for outcome in pack.outcomes:
        texts.append(outcome.brief.focus)
        texts.extend(outcome.brief.seed_queries)
        if outcome.specialist is SpecialistKind.PUBMED:
            continue
        texts.append(outcome.answer.answer)
        names.extend(_evidence_names(outcome.specialist_result))
    return collect_pmids(*texts, *names)


def _evidence_names(dump: dict[str, Any] | None) -> list[str]:
    if not dump:
        return []
    out: list[str] = []
    for note in dump.get("evidence") or []:
        if not isinstance(note, dict):
            continue
        pmid = note.get("pmid")
        if pmid:
            out.append(str(pmid))
        for name in note.get("names") or []:
            out.append(str(name))
    return out
