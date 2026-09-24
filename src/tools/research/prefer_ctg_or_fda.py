"""Decide CT.gov vs FDA source priority per NCT from research pack answers."""

from __future__ import annotations

from model.research.research_pack import ResearchPack
from model.research.specialist_kind import SpecialistKind
from tools.research.collect_nct_ids import collect_nct_ids


def prefer_ctg_or_fda(pack: ResearchPack) -> dict[str, str]:
    """Map NCT id → ``ctg`` | ``fda_fallback`` | ``unknown`` from pack answers."""
    fda_ncts = set()
    ctg_rich: set[str] = set()
    ctg_thin: set[str] = set()

    for outcome in pack.outcomes:
        text = outcome.answer.answer or ""
        ncts = set(
            collect_nct_ids(text, outcome.brief.focus, *outcome.brief.seed_queries)
        )
        if outcome.specialist is SpecialistKind.FDA_LABEL:
            fda_ncts |= ncts
            continue
        if outcome.specialist is not SpecialistKind.CTG:
            continue
        lower = text.lower()
        thin = any(
            phrase in lower
            for phrase in (
                "no results",
                "not posted",
                "no specific outcomes",
                "not provided",
                "no adverse",
            )
        )
        rich = any(
            token in lower
            for token in (
                "primary outcome",
                "secondary outcome",
                "objective response",
                "enrollment",
                "serious adverse",
            )
        )
        for nct in ncts:
            if rich and not thin:
                ctg_rich.add(nct)
            else:
                ctg_thin.add(nct)

    priority: dict[str, str] = {}
    for nct in sorted(fda_ncts | ctg_rich | ctg_thin):
        if nct in ctg_rich:
            priority[nct] = "ctg"
        elif nct in fda_ncts:
            priority[nct] = "fda_fallback"
        elif nct in ctg_thin:
            priority[nct] = "fda_fallback"
        else:
            priority[nct] = "unknown"
    return priority
