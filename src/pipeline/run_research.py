"""Pipeline entry for the research outer PEWE loop."""

from __future__ import annotations

import asyncio

from agents.research.run import run_research
from model.research.research_result import ResearchResult


def run_research_pipeline(
    brief: str,
    *,
    max_loops: int | None = None,
    run_id: str | None = None,
    concurrency: int | None = None,
    specialist_max_loops: int | None = None,
) -> ResearchResult:
    """Orchestrate research from pipeline/ (sync wrapper over async run)."""
    return asyncio.run(
        run_research(
            brief,
            max_loops=max_loops,
            run_id=run_id,
            concurrency=concurrency,
            specialist_max_loops=specialist_max_loops,
        )
    )
