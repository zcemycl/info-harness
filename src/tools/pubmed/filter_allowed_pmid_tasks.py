"""Keep only pubmed tasks whose PMID appears in the brief."""

from __future__ import annotations

from model.pubmed.is_placeholder_pmid import is_placeholder_pmid
from model.pubmed.pubmed_worker_plan import PubmedWorkerPlan
from tools.research.collect_pmids import collect_pmids


def filter_allowed_pmid_tasks(
    tasks: list[PubmedWorkerPlan],
    brief: str,
) -> tuple[list[PubmedWorkerPlan], list[str]]:
    """Drop invented/placeholder PMIDs; allow only ids present in the brief."""
    allowed = set(collect_pmids(brief))
    kept: list[PubmedWorkerPlan] = []
    rejected: list[str] = []
    for plan in tasks:
        pmid = plan.query.strip()
        if is_placeholder_pmid(pmid):
            rejected.append(f"rejected placeholder PMID {pmid}")
            continue
        if pmid not in allowed:
            rejected.append(f"rejected PMID {pmid} (not in brief; do not invent PMIDs)")
            continue
        kept.append(plan)
    return kept, rejected
