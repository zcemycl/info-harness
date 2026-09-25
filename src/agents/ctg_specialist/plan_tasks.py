"""Planner step for the CTG specialist PEWE loop."""

from __future__ import annotations

import json

from agents.chat_model import chat_model
from agents.invoke_schema_with_reader import invoke_schema_with_reader
from model.ctg.ctg_evidence_note import CtgEvidenceNote
from model.ctg.ctg_planner_output import CtgPlannerOutput
from model.research.diary_entry import DiaryEntry
from prompt.load_prompt import load_prompt
from tools.evidence.compact_evidence_notes import compact_evidence_notes
from tools.research.collect_nct_ids import collect_nct_ids


def plan_ctg_tasks(
    brief: str,
    *,
    loop: int,
    diary: list[DiaryEntry],
    evidence: list[CtgEvidenceNote],
) -> CtgPlannerOutput:
    """Ask the planner LLM for CtgWorkerPlan tasks."""
    llm = chat_model(model_env="OPENROUTER_FDA_SPECIALIST_MODEL")
    ncts_in_brief = collect_nct_ids(brief)
    payload = {
        "brief": brief,
        "loop": loop,
        "ncts_in_brief": ncts_in_brief,
        "routing_reminder": (
            "If ncts_in_brief is non-empty, plan worker=nctid or fetch for "
            "EACH listed NCT. When the brief asks for PubMed / literature / "
            "PMIDs / references, you MUST include worker=fetch with "
            "attrs=[references] (limit=20) for each NCT — references is "
            "fetch-only; worker=nctid cannot return PMIDs. Otherwise prefer "
            "attrs the brief needs (basic_info/outcomes/adverse_events/…). "
            "Do NOT use worker=condition or resolve_trial when NCT ids are "
            "already present. Never invent NCT ids or demo placeholders."
        ),
        "latest_diary": diary[-1].model_dump(mode="json") if diary else None,
        "evidence_tail": compact_evidence_notes(evidence),
    }
    return invoke_schema_with_reader(
        llm,
        CtgPlannerOutput,
        system=load_prompt("ctg", "specialist_planner.md"),
        user=json.dumps(payload, indent=2, default=str),
    )
