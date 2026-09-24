"""Writer step: compress PubMed worker pages into evidence notes."""

from __future__ import annotations

from typing import Any

from model.pubmed.pubmed_attr_hit import PubmedAttrHit
from model.pubmed.pubmed_attr_name import PubmedAttrName
from model.pubmed.pubmed_attr_page import PubmedAttrPage
from model.pubmed.pubmed_evidence_note import PubmedEvidenceNote
from model.pubmed.pubmed_worker_plan import PubmedWorkerPlan
from tools.diary.summarize_evidence_value import summarize_evidence_value


def write_pubmed_evidence_notes(
    triples: list[tuple[PubmedWorkerPlan, PubmedAttrName, PubmedAttrPage[Any]]],
    *,
    run_id: str,
) -> list[PubmedEvidenceNote]:
    """Turn executed pages into capped ledger notes with artifact pointers."""
    notes: list[PubmedEvidenceNote] = []
    for plan, attr, page in triples:
        for item in page.items:
            pmid = item.pmid if isinstance(item, PubmedAttrHit) else plan.query
            value = item.value if isinstance(item, PubmedAttrHit) else None
            summary, artifact_path, total = summarize_evidence_value(
                value,
                run_id=run_id,
                meta={
                    "worker": plan.worker.value,
                    "attr": attr.value,
                    "pmid": pmid,
                    "query": plan.query,
                },
            )
            notes.append(
                PubmedEvidenceNote(
                    worker=plan.worker,
                    query=plan.query,
                    attr=attr,
                    pmid=pmid,
                    names=_secondary_names(attr, item),
                    summary=summary or "hit",
                    artifact_path=artifact_path,
                    total_chars=total,
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
