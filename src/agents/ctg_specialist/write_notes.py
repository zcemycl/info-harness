"""Writer step: compress CTG worker results into evidence notes."""

from __future__ import annotations

from typing import Any

from model.ctg.ctg_attr_hit import CtgAttrHit
from model.ctg.ctg_attr_name import CtgAttrName
from model.ctg.ctg_attr_page import CtgAttrPage
from model.ctg.ctg_evidence_note import CtgEvidenceNote
from model.ctg.ctg_worker_plan import CtgWorkerName, CtgWorkerPlan
from model.ctg.resolved_trial import ResolvedTrial, ResolvedTrialStatus
from tools.diary.summarize_evidence_value import summarize_evidence_value


def write_ctg_evidence_notes(
    nctid_triples: list[tuple[CtgWorkerPlan, CtgAttrName, CtgAttrPage[Any]]],
    condition_pairs: list[tuple[CtgWorkerPlan, list[str]]],
    resolve_pairs: list[tuple[CtgWorkerPlan, ResolvedTrial]],
    *,
    run_id: str,
) -> list[CtgEvidenceNote]:
    """Turn executed pages/searches into compact ledger notes."""
    notes: list[CtgEvidenceNote] = []
    for plan, attr, page in nctid_triples:
        for item in page.items:
            nctid = item.nctid if isinstance(item, CtgAttrHit) else plan.query
            value = item.value if isinstance(item, CtgAttrHit) else None
            summary, artifact_path, total = summarize_evidence_value(
                value,
                run_id=run_id,
                meta={
                    "worker": plan.worker.value,
                    "attr": attr.value,
                    "nctid": nctid,
                    "query": plan.query,
                },
            )
            notes.append(
                CtgEvidenceNote(
                    worker=plan.worker,
                    query=plan.query,
                    attr=attr,
                    nctid=nctid,
                    setid=item.setid if isinstance(item, CtgAttrHit) else None,
                    names=_reference_pmids(attr, item),
                    summary=summary or f"{attr.value} hit",
                    artifact_path=artifact_path,
                    total_chars=total,
                    offset=page.offset,
                    next_offset=page.next_offset,
                )
            )
    for plan, names in condition_pairs:
        notes.append(_condition_note(plan, names))
    for plan, result in resolve_pairs:
        notes.append(_resolve_note(plan, result))
    return notes


def _condition_note(plan: CtgWorkerPlan, names: list[str]) -> CtgEvidenceNote:
    like = "%q%" if plan.both_sides else "q%"
    preview = ", ".join(names[:8])
    more = f" (+{len(names) - 8} more)" if len(names) > 8 else ""
    return CtgEvidenceNote(
        worker=CtgWorkerName.CONDITION,
        query=plan.query,
        names=names,
        both_sides=plan.both_sides,
        summary=f"{like} q={plan.query!r} → {len(names)} hit(s): {preview}{more}",
        total_chars=None,
    )


def _resolve_note(plan: CtgWorkerPlan, result: ResolvedTrial) -> CtgEvidenceNote:
    names = list(result.aliases_tried)
    if result.status is ResolvedTrialStatus.RESOLVED and result.nctid:
        summary = (
            f"resolved q={plan.query!r} → {result.nctid} "
            f"sources={result.sources} url={result.ctg_url}"
        )
    else:
        summary = (
            f"unresolved q={plan.query!r} sources={result.sources} "
            f"pmids={result.pmids[:5]}"
        )
    return CtgEvidenceNote(
        worker=CtgWorkerName.RESOLVE_TRIAL,
        query=plan.query,
        nctid=result.nctid,
        names=names,
        summary=summary,
    )


def _reference_pmids(attr: CtgAttrName, item: object) -> list[str]:
    """Extract PMIDs into names so the synthesizer sees them structurally."""
    if attr is not CtgAttrName.REFERENCES or not isinstance(item, CtgAttrHit):
        return []
    value = item.value
    if isinstance(value, dict):
        pmid = value.get("pmid")
        return [str(pmid).strip()] if pmid else []
    if not isinstance(value, list):
        return []
    pmids: list[str] = []
    seen: set[str] = set()
    for row in value:
        if not isinstance(row, dict):
            continue
        pmid = row.get("pmid")
        if pmid is None:
            continue
        text = str(pmid).strip()
        if text and text not in seen:
            seen.add(text)
            pmids.append(text)
    return pmids
