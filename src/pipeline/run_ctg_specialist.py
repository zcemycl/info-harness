"""Pipeline entry for the CTG specialist PEWE loop."""

from __future__ import annotations

from agents.ctg_specialist.run import run_ctg_specialist
from model.ctg.ctg_specialist_result import CtgSpecialistResult


def run_ctg_specialist_pipeline(
    brief: str,
    *,
    max_loops: int | None = None,
    run_id: str | None = None,
) -> CtgSpecialistResult:
    """Orchestrate the CTG specialist from pipeline/."""
    return run_ctg_specialist(brief, max_loops=max_loops, run_id=run_id)
