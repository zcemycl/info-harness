"""Planner step for the PubMed specialist PEWE loop."""

from __future__ import annotations

import json

from agents.chat_model import chat_model
from agents.invoke_schema_with_reader import invoke_schema_with_reader
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
    payload = {
        "brief": brief,
        "loop": loop,
        "routing_reminder": (
            "worker=id → numeric PMID + attrs. Query MUST appear "
            "verbatim in the brief (Known PMIDs / seed_queries). "
            "If the brief has no PMID, emit zero tasks — never invent. "
            "Prefer abstract (+ citation) when present; if abstract is "
            "null/empty, fetch citation + mesh/keywords/chemicals/"
            "publication_types/secondary_ids."
        ),
        "latest_diary": diary[-1].model_dump(mode="json") if diary else None,
        "evidence_tail": compact_evidence_notes(evidence),
    }
    return invoke_schema_with_reader(
        llm,
        PubmedPlannerOutput,
        system=load_prompt("pubmed", "specialist_planner.md"),
        user=json.dumps(payload, indent=2, default=str),
    )
