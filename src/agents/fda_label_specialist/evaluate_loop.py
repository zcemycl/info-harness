"""Evaluator step for the FDA label specialist PEWE loop."""

from __future__ import annotations

import json

from agents.chat_model import chat_model
from agents.invoke_schema_with_reader import invoke_schema_with_reader
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
    payload = {
        "brief": brief,
        "loop": loop,
        "evidence": compact_evidence_notes(evidence),
        "completeness_gaps": fda_completeness_gaps(evidence),
        "failures": failures or [],
    }
    entry = invoke_schema_with_reader(
        llm,
        DiaryEntry,
        system=load_prompt("fda", "specialist_evaluator.md"),
        user=json.dumps(payload, indent=2, default=str),
    )
    return entry.model_copy(update={"loop": loop})
