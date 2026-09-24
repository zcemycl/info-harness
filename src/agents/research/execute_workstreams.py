"""Async parallel executor: spawn selected research workstreams."""

from __future__ import annotations

import asyncio
import os

from agents.research.ensure_workstream_ids import ensure_workstream_ids
from agents.research.fingerprint_idea import fingerprint_brief
from agents.research.spawn_specialist import spawn_specialist_sync
from model.research.research_outcome import ResearchOutcome
from model.research.research_pack import ResearchPack
from model.research.research_plan import ResearchPlan
from model.research.specialist_brief import SpecialistBrief

DEFAULT_CONCURRENCY = int(os.getenv("RESEARCH_SPECIALIST_CONCURRENCY", "3"))


async def execute_workstreams(
    plan: ResearchPlan,
    *,
    run_id: str,
    concurrency: int = DEFAULT_CONCURRENCY,
    specialist_max_loops: int | None = None,
) -> ResearchPack:
    """Spawn unique workstreams in parallel via asyncio.to_thread + semaphore."""
    if concurrency < 1:
        raise ValueError(f"concurrency must be >= 1, got {concurrency}")

    briefs = _unique_briefs(ensure_workstream_ids(plan.selected))
    semaphore = asyncio.Semaphore(concurrency)

    async def _one(brief: SpecialistBrief) -> ResearchOutcome:
        async with semaphore:
            return await asyncio.to_thread(
                spawn_specialist_sync,
                brief,
                run_id=run_id,
                specialist_max_loops=specialist_max_loops,
            )

    outcomes = await asyncio.gather(*(_one(b) for b in briefs))
    return ResearchPack(outcomes=list(outcomes))


def _unique_briefs(briefs: list[SpecialistBrief]) -> list[SpecialistBrief]:
    """De-dupe by workstream_id, then by idea fingerprint (first wins)."""
    seen_ids: set[str] = set()
    seen_fps: set[str] = set()
    unique: list[SpecialistBrief] = []
    for brief in briefs:
        wid = brief.workstream_id or ""
        fp = fingerprint_brief(brief)
        if wid in seen_ids or fp in seen_fps:
            continue
        seen_ids.add(wid)
        seen_fps.add(fp)
        unique.append(brief)
    return unique
