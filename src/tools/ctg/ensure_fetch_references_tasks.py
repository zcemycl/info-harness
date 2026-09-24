"""Append live fetch+references tasks when literature PMIDs are needed."""

from __future__ import annotations

from model.ctg.ctg_attr_name import CtgAttrName
from model.ctg.ctg_worker_plan import CtgWorkerName, CtgWorkerPlan
from tools.research.brief_wants_literature import brief_wants_literature
from tools.research.collect_nct_ids import collect_nct_ids


def ensure_fetch_references_tasks(
    tasks: list[CtgWorkerPlan],
    brief: str,
) -> list[CtgWorkerPlan]:
    """If brief wants literature, ensure worker=fetch attrs=[references] per NCT."""
    if not brief_wants_literature(brief):
        return tasks
    ncts = list(
        dict.fromkeys(
            [
                *collect_nct_ids(brief),
                *[
                    t.query.strip().upper()
                    for t in tasks
                    if t.worker in (CtgWorkerName.NCTID, CtgWorkerName.FETCH)
                ],
            ]
        )
    )
    if not ncts:
        return tasks
    out = list(tasks)
    for nct in ncts:
        if _has_fetch_references(out, nct):
            continue
        out.append(
            CtgWorkerPlan(
                worker=CtgWorkerName.FETCH,
                query=nct,
                attrs=[CtgAttrName.REFERENCES],
                offset=0,
                limit=20,
            )
        )
    return out


def _has_fetch_references(tasks: list[CtgWorkerPlan], nct: str) -> bool:
    target = nct.strip().upper()
    for plan in tasks:
        if plan.worker is not CtgWorkerName.FETCH:
            continue
        if plan.query.strip().upper() != target:
            continue
        if CtgAttrName.REFERENCES in plan.attrs:
            return True
    return False
