"""Pipeline entry for the PubMed specialist PEWE loop."""

from __future__ import annotations

from agents.pubmed_specialist.run import run_pubmed_specialist
from model.pubmed.pubmed_specialist_result import PubmedSpecialistResult


def run_pubmed_specialist_pipeline(
    brief: str,
    *,
    max_loops: int | None = None,
    run_id: str | None = None,
) -> PubmedSpecialistResult:
    """Orchestrate the PubMed specialist from pipeline/."""
    return run_pubmed_specialist(brief, max_loops=max_loops, run_id=run_id)
