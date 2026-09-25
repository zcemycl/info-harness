"""Evaluator step for the ICD therapeutic-area specialist PEWE loop."""

from __future__ import annotations

import json

from agents.chat_model import chat_model
from agents.invoke_schema_with_reader import invoke_schema_with_reader
from model.research.diary_entry import DiaryEntry
from model.therapeutic_area.icd_evidence_note import IcdEvidenceNote
from prompt.load_prompt import load_prompt


def evaluate_icd_loop(
    brief: str,
    *,
    loop: int,
    evidence: list[IcdEvidenceNote],
    failures: list[str] | None = None,
) -> DiaryEntry:
    """Ask the evaluator LLM for a DiaryEntry decision."""
    llm = chat_model(model_env="OPENROUTER_FDA_SPECIALIST_MODEL")
    payload = {
        "brief": brief,
        "loop": loop,
        "evidence": [n.model_dump(mode="json") for n in evidence],
        "failures": failures or [],
    }
    entry = invoke_schema_with_reader(
        llm,
        DiaryEntry,
        system=load_prompt("therapeutic_area", "specialist_evaluator.md"),
        user=json.dumps(payload, indent=2, default=str),
    )
    return entry.model_copy(update={"loop": loop})
