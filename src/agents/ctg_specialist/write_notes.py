"""Writer step: compress CTG worker results into evidence notes."""

from __future__ import annotations

import json
from typing import Any

from model.ctg.ctg_attr_hit import CtgAttrHit
from model.ctg.ctg_attr_name import CtgAttrName
from model.ctg.ctg_attr_page import CtgAttrPage
from model.ctg.ctg_evidence_note import CtgEvidenceNote
from model.ctg.ctg_worker_plan import CtgWorkerName, CtgWorkerPlan
from model.ctg.resolved_trial import ResolvedTrial, ResolvedTrialStatus


def write_ctg_evidence_notes(
    nctid_triples: list[tuple[CtgWorkerPlan, CtgAttrName, CtgAttrPage[Any]]],
    condition_pairs: list[tuple[CtgWorkerPlan, list[str]]],
    resolve_pairs: list[tuple[CtgWorkerPlan, ResolvedTrial]],
) -> list[CtgEvidenceNote]:
    """Turn executed pages/searches into compact ledger notes."""
    notes: list[CtgEvidenceNote] = []
    for plan, attr, page in nctid_triples:
        for item in page.items:
            notes.append(
                CtgEvidenceNote(
                    worker=CtgWorkerName.NCTID,
                    query=plan.query,
                    attr=attr,
                    nctid=item.nctid if isinstance(item, CtgAttrHit) else plan.query,
                    setid=item.setid if isinstance(item, CtgAttrHit) else None,
                    summary=_nctid_summary(attr, item),
                    offset=page.offset,
                    next_offset=page.next_offset,
                )
            )
    for plan, names in condition_pairs:
        like = "%q%" if plan.both_sides else "q%"
        preview = ", ".join(names[:8])
        more = f" (+{len(names) - 8} more)" if len(names) > 8 else ""
        notes.append(
            CtgEvidenceNote(
                worker=CtgWorkerName.CONDITION,
                query=plan.query,
                names=names,
                both_sides=plan.both_sides,
                summary=(
                    f"{like} q={plan.query!r} → {len(names)} hit(s): "
                    f"{preview}{more}"
                ),
            )
        )
    for plan, result in resolve_pairs:
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
        notes.append(
            CtgEvidenceNote(
                worker=CtgWorkerName.RESOLVE_TRIAL,
                query=plan.query,
                nctid=result.nctid,
                names=names,
                summary=summary,
            )
        )
    return notes


def _nctid_summary(attr: CtgAttrName, item: object) -> str:
    if isinstance(item, CtgAttrHit):
        return _value_summary(item.value)[:400]
    return f"{attr.value} hit"


def _value_summary(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return ", ".join(str(v) for v in value[:5])
    if hasattr(value, "model_dump"):
        dumped = value.model_dump(mode="json")  # type: ignore[union-attr]
        return json.dumps(dumped, default=str)
    return json.dumps(value, default=str)
