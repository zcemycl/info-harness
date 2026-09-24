"""Inject known NCT ids into CTG specialist briefs before spawn."""

from __future__ import annotations

from model.research.specialist_brief import SpecialistBrief
from model.research.specialist_kind import SpecialistKind
from tools.research.collect_nct_ids import collect_nct_ids


def enrich_ctg_briefs(
    briefs: list[SpecialistBrief],
    known_ncts: list[str],
) -> list[SpecialistBrief]:
    """Ensure CTG focuses/seeds list known NCTs; skip when none known."""
    if not known_ncts:
        return briefs
    out: list[SpecialistBrief] = []
    for brief in briefs:
        if brief.specialist is not SpecialistKind.CTG:
            out.append(brief)
            continue
        already = set(collect_nct_ids(brief.focus, *brief.seed_queries))
        missing = [n for n in known_ncts if n not in already]
        if not missing:
            out.append(brief)
            continue
        seeds = list(dict.fromkeys([*brief.seed_queries, *known_ncts]))
        note = (
            "Known NCT ids (use worker=nctid or fetch for each; do not "
            "search by drug name alone): " + ", ".join(known_ncts)
        )
        focus = brief.focus.rstrip()
        if "Known NCT ids" not in focus:
            focus = f"{focus}\n\n{note}"
        out.append(brief.model_copy(update={"focus": focus, "seed_queries": seeds}))
    return out
