"""Assign stable workstream ids when the planner omits them."""

from __future__ import annotations

from agents.research.fingerprint_idea import fingerprint_brief
from model.research.specialist_brief import SpecialistBrief


def ensure_workstream_ids(briefs: list[SpecialistBrief]) -> list[SpecialistBrief]:
    """Fill missing workstream_id from specialist + idea fingerprint."""
    seen: set[str] = set()
    out: list[SpecialistBrief] = []
    for brief in briefs:
        wid = (brief.workstream_id or "").strip()
        if not wid:
            wid = f"{brief.specialist.value}-{fingerprint_brief(brief)}"
        base = wid
        n = 2
        while wid in seen:
            wid = f"{base}-{n}"
            n += 1
        seen.add(wid)
        out.append(brief.model_copy(update={"workstream_id": wid}))
    return out
