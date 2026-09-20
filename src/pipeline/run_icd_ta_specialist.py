"""Pipeline entry for the ICD therapeutic-area specialist PEWE loop."""

from __future__ import annotations

from agents.icd_ta_specialist.run import run_icd_ta_specialist
from model.therapeutic_area.icd_specialist_result import IcdSpecialistResult


def run_icd_ta_specialist_pipeline(
    brief: str,
    *,
    max_loops: int | None = None,
    run_id: str | None = None,
) -> IcdSpecialistResult:
    """Orchestrate the ICD TA specialist from pipeline/."""
    return run_icd_ta_specialist(brief, max_loops=max_loops, run_id=run_id)
