"""Drop pubmed workstreams that lack real PMIDs; route CTG first."""

from __future__ import annotations

from model.research.specialist_brief import SpecialistBrief
from model.research.specialist_kind import SpecialistKind
from tools.research.collect_pmids import collect_pmids


def gate_pubmed_briefs(
    briefs: list[SpecialistBrief],
    *,
    user_brief: str = "",
) -> list[SpecialistBrief]:
    """Remove pubmed briefs with no PMIDs; add CTG when pubmed was the only path."""
    kept: list[SpecialistBrief] = []
    dropped_pubmed = False
    for brief in briefs:
        if brief.specialist is not SpecialistKind.PUBMED:
            kept.append(brief)
            continue
        pmids = collect_pmids(brief.focus, *brief.seed_queries, user_brief)
        if pmids:
            kept.append(brief)
        else:
            dropped_pubmed = True
    if not dropped_pubmed:
        return kept
    has_upstream = any(
        b.specialist in (SpecialistKind.CTG, SpecialistKind.FDA_LABEL) for b in kept
    )
    if has_upstream:
        return kept
    focus = (
        "Literature / PubMed handoff: resolve pivotal NCT ids for this "
        "brief if needed, then worker=fetch with attrs=[references] "
        f"(limit=20) for each NCT. Return PMIDs.\n\nUser brief: "
        f"{user_brief.strip()}"
    )
    kept.append(
        SpecialistBrief(
            specialist=SpecialistKind.CTG,
            focus=focus,
            seed_queries=[],
            workstream_id="ctg-for-pubmed-refs",
        )
    )
    return kept
