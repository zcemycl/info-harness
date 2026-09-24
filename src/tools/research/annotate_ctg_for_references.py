"""Annotate CTG briefs to require live fetch references for literature."""

from __future__ import annotations

from model.research.specialist_brief import SpecialistBrief
from model.research.specialist_kind import SpecialistKind
from tools.research.brief_wants_literature import brief_wants_literature


def annotate_ctg_for_references(
    briefs: list[SpecialistBrief],
    *,
    user_brief: str = "",
) -> list[SpecialistBrief]:
    """When literature is requested, require worker=fetch + references on CTG."""
    if not brief_wants_literature(user_brief, *[b.focus for b in briefs]):
        return briefs
    note = (
        "Literature requested: for each known NCT use worker=fetch with "
        "attrs=[references] (limit=20). references is fetch-only — do not "
        "use worker=nctid alone. Return PMIDs for PubMed handoff."
    )
    out: list[SpecialistBrief] = []
    for brief in briefs:
        if brief.specialist is not SpecialistKind.CTG:
            out.append(brief)
            continue
        focus = brief.focus.rstrip()
        if "attrs=[references]" in focus or "worker=fetch" in focus.lower():
            out.append(brief)
            continue
        out.append(brief.model_copy(update={"focus": f"{focus}\n\n{note}"}))
    return out
