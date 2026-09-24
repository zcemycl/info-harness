"""Inject known PMIDs into PubMed specialist briefs before spawn."""

from __future__ import annotations

from model.research.specialist_brief import SpecialistBrief
from model.research.specialist_kind import SpecialistKind
from tools.research.collect_pmids import collect_pmids


def enrich_pubmed_briefs(
    briefs: list[SpecialistBrief],
    known_pmids: list[str],
) -> list[SpecialistBrief]:
    """Ensure pubmed focuses/seeds list known PMIDs; skip when none known."""
    if not known_pmids:
        return briefs
    out: list[SpecialistBrief] = []
    for brief in briefs:
        if brief.specialist is not SpecialistKind.PUBMED:
            out.append(brief)
            continue
        already = set(collect_pmids(brief.focus, *brief.seed_queries))
        missing = [p for p in known_pmids if p not in already]
        if not missing:
            out.append(brief)
            continue
        seeds = list(dict.fromkeys([*brief.seed_queries, *known_pmids]))
        note = "Known PMIDs (worker=id only; do not invent others): " + ", ".join(
            known_pmids
        )
        focus = brief.focus.rstrip()
        if "Known PMIDs" not in focus:
            focus = f"{focus}\n\n{note}"
        out.append(brief.model_copy(update={"focus": focus, "seed_queries": seeds}))
    return out
