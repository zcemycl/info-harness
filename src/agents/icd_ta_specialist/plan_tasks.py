"""Planner step for the ICD therapeutic-area specialist PEWE loop."""

from __future__ import annotations

import json

from agents.chat_model import chat_model
from agents.invoke_schema_with_reader import invoke_schema_with_reader
from model.research.diary_entry import DiaryEntry
from model.therapeutic_area.icd_evidence_note import IcdEvidenceNote
from model.therapeutic_area.icd_planner_output import IcdPlannerOutput
from prompt.load_prompt import load_prompt


def plan_icd_tasks(
    brief: str,
    *,
    loop: int,
    diary: list[DiaryEntry],
    evidence: list[IcdEvidenceNote],
) -> IcdPlannerOutput:
    """Ask the planner LLM for IcdWorkerPlan search tasks."""
    llm = chat_model(model_env="OPENROUTER_FDA_SPECIALIST_MODEL")
    payload = {
        "brief": brief,
        "loop": loop,
        "routing_reminder": (
            "Only tool: search_therapeutic_area. "
            "both_sides=false → SQL LIKE q% (prefix). "
            "both_sides=true → SQL LIKE %q% (either side). "
            "Prefer prefix first; flip both_sides on miss."
        ),
        "latest_diary": diary[-1].model_dump(mode="json") if diary else None,
        "evidence_tail": [n.model_dump(mode="json") for n in evidence[-20:]],
    }
    return invoke_schema_with_reader(
        llm,
        IcdPlannerOutput,
        system=load_prompt("therapeutic_area", "specialist_planner.md"),
        user=json.dumps(payload, indent=2, default=str),
    )
