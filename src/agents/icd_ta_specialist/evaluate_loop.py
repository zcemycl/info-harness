"""Evaluator step for the ICD therapeutic-area specialist PEWE loop."""

from __future__ import annotations

import json

from agents.chat_model import chat_model
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
    structured = llm.with_structured_output(DiaryEntry)
    payload = {
        "brief": brief,
        "loop": loop,
        "evidence": [n.model_dump(mode="json") for n in evidence],
        "failures": failures or [],
    }
    result = structured.invoke(
        [
            {
                "role": "system",
                "content": load_prompt("therapeutic_area", "specialist_evaluator.md"),
            },
            {
                "role": "user",
                "content": json.dumps(payload, indent=2, default=str),
            },
        ]
    )
    entry = (
        result if isinstance(result, DiaryEntry) else DiaryEntry.model_validate(result)
    )
    return entry.model_copy(update={"loop": loop})
