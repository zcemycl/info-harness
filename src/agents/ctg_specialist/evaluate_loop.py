"""Evaluator step for the CTG specialist PEWE loop."""

from __future__ import annotations

import json

from agents.chat_model import chat_model
from model.ctg.ctg_evidence_note import CtgEvidenceNote
from model.research.diary_entry import DiaryEntry
from prompt.load_prompt import load_prompt
from tools.evidence.compact_evidence_notes import compact_evidence_notes


def evaluate_ctg_loop(
    brief: str,
    *,
    loop: int,
    evidence: list[CtgEvidenceNote],
    failures: list[str] | None = None,
) -> DiaryEntry:
    """Ask the evaluator LLM for a DiaryEntry decision."""
    llm = chat_model(model_env="OPENROUTER_FDA_SPECIALIST_MODEL")
    structured = llm.with_structured_output(DiaryEntry)
    payload = {
        "brief": brief,
        "loop": loop,
        "evidence": compact_evidence_notes(evidence),
        "failures": failures or [],
    }
    result = structured.invoke(
        [
            {
                "role": "system",
                "content": load_prompt("ctg", "specialist_evaluator.md"),
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
