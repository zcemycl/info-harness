"""Writer step: compress worker pages into EvidenceNote rows."""

from __future__ import annotations

import json
from typing import Any

from model.fda.fda_label_attr_hit import FdaLabelAttrHit
from model.fda.fda_label_attr_page import FdaLabelAttrPage
from model.fda.fda_label_section import FdaLabelSection
from model.research.evidence_note import EvidenceNote
from model.research.worker_plan import FdaAttrName, WorkerPlan
from tools.diary.summarize_evidence_value import summarize_evidence_value
from tools.fda.extract_ctg_nct_links import extract_ctg_nct_links
from tools.fda.extract_study_mentions import extract_study_mentions

_FDA_SUMMARY_MAX = 400


def write_evidence_notes(
    triples: list[tuple[WorkerPlan, FdaAttrName, FdaLabelAttrPage[Any]]],
    *,
    run_id: str,
) -> list[EvidenceNote]:
    """Turn executed pages into compact ledger notes (deterministic)."""
    notes: list[EvidenceNote] = []
    for plan, attr, page in triples:
        for item in page.items:
            summary, artifact_path, total = _item_summary(attr, item, run_id=run_id)
            notes.append(
                EvidenceNote(
                    worker=plan.worker,
                    attr=attr,
                    query=plan.query,
                    label_id=item.id,
                    setid=item.setid,
                    tradename=item.tradename,
                    summary=summary,
                    artifact_path=artifact_path,
                    total_chars=total,
                    offset=page.offset,
                    next_offset=page.next_offset,
                )
            )
    return notes


def _item_summary(
    attr: FdaAttrName, item: object, *, run_id: str
) -> tuple[str, str | None, int | None]:
    if not isinstance(item, FdaLabelAttrHit):
        return f"{attr.value} hit", None, None
    raw = _value_text(item.value)
    summary, artifact_path, total = summarize_evidence_value(
        raw,
        run_id=run_id,
        meta={
            "worker": "fda",
            "attr": attr.value,
            "label_id": item.id,
            "setid": str(item.setid),
            "tradename": item.tradename,
        },
        max_chars=_FDA_SUMMARY_MAX,
    )
    extras: list[str] = []
    links = extract_ctg_nct_links(raw)
    if links:
        extras.append(
            "CTG links: " + "; ".join(f"{link.nctid} {link.ctg_url}" for link in links)
        )
    mentions = extract_study_mentions(raw)
    if mentions:
        extras.append(
            "Study mentions: "
            + "; ".join(f"{m.raw} ({m.kind.value})" for m in mentions[:12])
        )
    if extras:
        summary = "\n".join([summary, *extras])
    return summary, artifact_path, total


def _value_text(value: object) -> str:
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
