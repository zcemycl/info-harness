"""Evaluator step for the FDA label specialist PEWE loop."""

from __future__ import annotations

import json

from agents.chat_model import chat_model
from model.research.diary_entry import DiaryEntry
from model.research.evidence_note import EvidenceNote
from prompt.load_prompt import load_prompt
from tools.evidence.compact_evidence_notes import compact_evidence_notes
from tools.fda.fda_completeness_gaps import fda_completeness_gaps


def evaluate_fda_loop(
    brief: str,
    *,
    loop: int,
    evidence: list[EvidenceNote],
    failures: list[str] | None = None,
) -> DiaryEntry:
    """Ask the evaluator LLM for a DiaryEntry decision."""
    llm = chat_model(model_env="OPENROUTER_FDA_SPECIALIST_MODEL")
    structured = llm.with_structured_output(DiaryEntry)
    payload = {
        "brief": brief,
        "loop": loop,
        "evidence": compact_evidence_notes(evidence),
        "completeness_gaps": fda_completeness_gaps(evidence),
        "failures": failures or [],
    }
    result = structured.invoke(
        [
            {
                "role": "system",
                "content": load_prompt("fda", "specialist_evaluator.md"),
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
