"""Writer step: compress worker pages into EvidenceNote rows."""

from __future__ import annotations

from typing import Any

from model.fda.fda_label_adverse_effects_hit import FdaLabelAdverseEffectsHit
from model.fda.fda_label_attr_page import FdaLabelAttrPage
from model.fda.fda_label_indication_hit import FdaLabelIndicationHit
from model.research.evidence_note import EvidenceNote
from model.research.worker_plan import FdaAttrName, WorkerPlan


def write_evidence_notes(
    triples: list[tuple[WorkerPlan, FdaAttrName, FdaLabelAttrPage[Any]]],
) -> list[EvidenceNote]:
    """Turn executed pages into compact ledger notes (deterministic)."""
    notes: list[EvidenceNote] = []
    for plan, attr, page in triples:
        for item in page.items:
            notes.append(
                EvidenceNote(
                    worker=plan.worker,
                    attr=attr,
                    query=plan.query,
                    label_id=item.id,
                    setid=item.setid,
                    tradename=item.tradename,
                    summary=_summary(attr, item),
                    offset=page.offset,
                    next_offset=page.next_offset,
                )
            )
    return notes


def _summary(attr: FdaAttrName, item: object) -> str:
    if isinstance(item, FdaLabelIndicationHit):
        return (item.indication or "")[:400]
    if isinstance(item, FdaLabelAdverseEffectsHit):
        sections = item.adverse_effects or []
        parts = [s.content or "" for s in sections[:2]]
        return " ".join(parts)[:400]
    return f"{attr.value} hit"
