"""Evaluator step for the CTG specialist PEWE loop."""

from __future__ import annotations

import json

from agents.chat_model import chat_model
from agents.invoke_schema_with_reader import invoke_schema_with_reader
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
    payload = {
        "brief": brief,
        "loop": loop,
        "evidence": compact_evidence_notes(evidence),
        "failures": failures or [],
    }
    entry = invoke_schema_with_reader(
        llm,
        DiaryEntry,
        system=load_prompt("ctg", "specialist_evaluator.md"),
        user=json.dumps(payload, indent=2, default=str),
    )
    return entry.model_copy(update={"loop": loop})
