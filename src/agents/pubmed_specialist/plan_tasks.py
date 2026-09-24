"""Planner step for the PubMed specialist PEWE loop."""

from __future__ import annotations

import json

from agents.chat_model import chat_model
from model.pubmed.pubmed_evidence_note import PubmedEvidenceNote
from model.pubmed.pubmed_planner_output import PubmedPlannerOutput
from model.research.diary_entry import DiaryEntry
from prompt.load_prompt import load_prompt
from tools.evidence.compact_evidence_notes import compact_evidence_notes


def plan_pubmed_tasks(
    brief: str,
    *,
    loop: int,
    diary: list[DiaryEntry],
    evidence: list[PubmedEvidenceNote],
) -> PubmedPlannerOutput:
    """Ask the planner LLM for PubmedWorkerPlan tasks."""
    llm = chat_model(model_env="OPENROUTER_FDA_SPECIALIST_MODEL")
    structured = llm.with_structured_output(PubmedPlannerOutput)
    payload = {
        "brief": brief,
        "loop": loop,
        "routing_reminder": (
            "worker=id → numeric PMID + attrs. "
            "For CT.gov-empty outcomes prefer abstract (+ citation). "
            "Never invent PMIDs."
        ),
        "latest_diary": diary[-1].model_dump(mode="json") if diary else None,
        "evidence_tail": compact_evidence_notes(evidence),
    }
    result = structured.invoke(
        [
            {
                "role": "system",
                "content": load_prompt("pubmed", "specialist_planner.md"),
            },
            {
                "role": "user",
                "content": json.dumps(payload, indent=2, default=str),
            },
        ]
    )
    if isinstance(result, PubmedPlannerOutput):
        return result
    return PubmedPlannerOutput.model_validate(result)
