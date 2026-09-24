"""Planner step for the CTG specialist PEWE loop."""

from __future__ import annotations

import json

from agents.chat_model import chat_model
from model.ctg.ctg_evidence_note import CtgEvidenceNote
from model.ctg.ctg_planner_output import CtgPlannerOutput
from model.research.diary_entry import DiaryEntry
from prompt.load_prompt import load_prompt
from tools.evidence.compact_evidence_notes import compact_evidence_notes


def plan_ctg_tasks(
    brief: str,
    *,
    loop: int,
    diary: list[DiaryEntry],
    evidence: list[CtgEvidenceNote],
) -> CtgPlannerOutput:
    """Ask the planner LLM for CtgWorkerPlan tasks."""
    llm = chat_model(model_env="OPENROUTER_FDA_SPECIALIST_MODEL")
    structured = llm.with_structured_output(CtgPlannerOutput)
    payload = {
        "brief": brief,
        "loop": loop,
        "routing_reminder": (
            "worker=nctid → real NCT######## + HC attrs. "
            "worker=fetch → real NCT######## live CT.gov (incl. references). "
            "worker=condition → condition phrase autocomplete (both_sides). "
            "Never invent NCT ids. Never use demo placeholders "
            "(NCT01234567 / NCT01234569 / ascending digits)."
        ),
        "latest_diary": diary[-1].model_dump(mode="json") if diary else None,
        "evidence_tail": compact_evidence_notes(evidence),
    }
    result = structured.invoke(
        [
            {"role": "system", "content": load_prompt("ctg", "specialist_planner.md")},
            {
                "role": "user",
                "content": json.dumps(payload, indent=2, default=str),
            },
        ]
    )
    if isinstance(result, CtgPlannerOutput):
        return result
    return CtgPlannerOutput.model_validate(result)
