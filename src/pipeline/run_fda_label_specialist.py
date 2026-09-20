"""Pipeline entry for the FDA label specialist PEWE loop."""

from __future__ import annotations

from agents.fda_label_specialist.run import run_fda_label_specialist
from model.research.fda_specialist_result import FdaSpecialistResult


def run_fda_label_specialist_pipeline(
    brief: str,
    *,
    max_loops: int | None = None,
    run_id: str | None = None,
) -> FdaSpecialistResult:
    """Orchestrate the FDA label specialist from pipeline/."""
    return run_fda_label_specialist(brief, max_loops=max_loops, run_id=run_id)
