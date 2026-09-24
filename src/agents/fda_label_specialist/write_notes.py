"""Writer step: compress worker pages into EvidenceNote rows."""

from __future__ import annotations

import json
from typing import Any

from model.fda.fda_label_attr_hit import FdaLabelAttrHit
from model.fda.fda_label_attr_page import FdaLabelAttrPage
from model.fda.fda_label_section import FdaLabelSection
from model.research.evidence_note import EvidenceNote
from model.research.worker_plan import FdaAttrName, WorkerPlan
from tools.fda.extract_ctg_nct_links import extract_ctg_nct_links
from tools.fda.extract_study_mentions import extract_study_mentions


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
    if isinstance(item, FdaLabelAttrHit):
        raw = _value_summary(item.value)
        excerpt = raw[:400]
        parts = [excerpt]
        links = extract_ctg_nct_links(raw)
        if links:
            link_bits = "; ".join(f"{link.nctid} {link.ctg_url}" for link in links)
            parts.append(f"CTG links: {link_bits}")
        mentions = extract_study_mentions(raw)
        if mentions:
            mention_bits = "; ".join(f"{m.raw} ({m.kind.value})" for m in mentions[:12])
            parts.append(f"Study mentions: {mention_bits}")
        return "\n".join(parts)
    return f"{attr.value} hit"


def _value_summary(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        parts: list[str] = []
        for entry in value[:3]:
            if isinstance(entry, FdaLabelSection):
                parts.append(entry.content or "")
            elif hasattr(entry, "caption"):
                parts.append(str(getattr(entry, "caption", "")))
            elif hasattr(entry, "name"):
                parts.append(str(getattr(entry, "name", "")))
            else:
                parts.append(str(entry))
        return " ".join(parts)
    if hasattr(value, "model_dump"):
        dumped = value.model_dump(mode="json")  # type: ignore[union-attr]
        return json.dumps(dumped, default=str)
    return str(value)
