"""Planner step for the FDA label specialist PEWE loop."""

from __future__ import annotations

import json

from agents.chat_model import chat_model
from model.research.diary_entry import DiaryEntry
from model.research.evidence_note import EvidenceNote
from model.research.planner_output import PlannerOutput
from prompt.load_prompt import load_prompt


def plan_fda_tasks(
    brief: str,
    *,
    loop: int,
    diary: list[DiaryEntry],
    evidence: list[EvidenceNote],
) -> PlannerOutput:
    """Ask the planner LLM for WorkerPlan tasks (fixed worker/attr enums)."""
    llm = chat_model(model_env="OPENROUTER_FDA_SPECIALIST_MODEL")
    structured = llm.with_structured_output(PlannerOutput)
    payload = {
        "brief": brief,
        "loop": loop,
        "routing_reminder": (
            "worker=tradename → brand name only (Keytruda). "
            "worker=indication → disease/condition only (HIV, melanoma). "
            "Never set worker=tradename with query=HIV."
        ),
        "latest_diary": diary[-1].model_dump(mode="json") if diary else None,
        "evidence_tail": [n.model_dump(mode="json") for n in evidence[-20:]],
    }
    result = structured.invoke(
        [
            {"role": "system", "content": load_prompt("fda", "specialist_planner.md")},
            {
                "role": "user",
                "content": json.dumps(payload, indent=2, default=str),
            },
        ]
    )
    if isinstance(result, PlannerOutput):
        return result
    return PlannerOutput.model_validate(result)
