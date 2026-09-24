"""Merge prior research outcomes into the current outer-loop pack."""

from __future__ import annotations

from model.research.research_outcome import ResearchOutcome
from model.research.research_pack import ResearchPack


def merge_prior_pack(
    current: ResearchPack,
    prior: ResearchPack | None,
) -> ResearchPack:
    """Keep prior outcomes for workstreams not re-spawned this loop.

    Current outcomes always replace prior entries with the same workstream_id.
    """
    if prior is None or not prior.outcomes:
        return current

    by_id: dict[str, ResearchOutcome] = {}
    order: list[str] = []
    for item in prior.outcomes:
        if item.workstream_id not in by_id:
            order.append(item.workstream_id)
        by_id[item.workstream_id] = item
    for item in current.outcomes:
        if item.workstream_id not in by_id:
            order.append(item.workstream_id)
        by_id[item.workstream_id] = item
    return ResearchPack(outcomes=[by_id[key] for key in order])
