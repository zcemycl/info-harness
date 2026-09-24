"""Writer step: compress PubMed worker pages into evidence notes."""

from __future__ import annotations

import json
from typing import Any

from model.pubmed.pubmed_attr_hit import PubmedAttrHit
from model.pubmed.pubmed_attr_name import PubmedAttrName
from model.pubmed.pubmed_attr_page import PubmedAttrPage
from model.pubmed.pubmed_evidence_note import PubmedEvidenceNote
from model.pubmed.pubmed_worker_plan import PubmedWorkerPlan


def write_pubmed_evidence_notes(
    triples: list[tuple[PubmedWorkerPlan, PubmedAttrName, PubmedAttrPage[Any]]],
) -> list[PubmedEvidenceNote]:
    """Turn executed pages into ledger notes (no truncation)."""
    notes: list[PubmedEvidenceNote] = []
    for plan, attr, page in triples:
        for item in page.items:
            notes.append(
                PubmedEvidenceNote(
                    worker=plan.worker,
                    query=plan.query,
                    attr=attr,
                    pmid=item.pmid if isinstance(item, PubmedAttrHit) else plan.query,
                    names=_secondary_names(attr, item),
                    summary=_summary(item),
                    offset=page.offset,
                    next_offset=page.next_offset,
                )
            )
    return notes


def _secondary_names(attr: PubmedAttrName, item: object) -> list[str]:
    if attr is not PubmedAttrName.SECONDARY_IDS or not isinstance(item, PubmedAttrHit):
        return []
    value = item.value
    if isinstance(value, dict) and value.get("value"):
        return [str(value["value"])]
    return []


def _summary(item: object) -> str:
    if not isinstance(item, PubmedAttrHit):
        return "hit"
    value = item.value
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return json.dumps(value, default=str)
