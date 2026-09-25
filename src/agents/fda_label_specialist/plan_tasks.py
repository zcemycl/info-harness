"""Planner step for the FDA label specialist PEWE loop."""

from __future__ import annotations

import json

from agents.chat_model import chat_model
from agents.invoke_schema_with_reader import invoke_schema_with_reader
from model.research.diary_entry import DiaryEntry
from model.research.evidence_note import EvidenceNote
from model.research.planner_output import PlannerOutput
from prompt.load_prompt import load_prompt
from tools.evidence.compact_evidence_notes import compact_evidence_notes
from tools.fda.fda_completeness_gaps import fda_completeness_gaps


def plan_fda_tasks(
    brief: str,
    *,
    loop: int,
    diary: list[DiaryEntry],
    evidence: list[EvidenceNote],
) -> PlannerOutput:
    """Ask the planner LLM for WorkerPlan tasks (fixed worker/attr enums)."""
    llm = chat_model(model_env="OPENROUTER_FDA_SPECIALIST_MODEL")
    payload = {
        "brief": brief,
        "loop": loop,
        "routing_reminder": (
            "worker=tradename → brand name only (Keytruda). "
            "worker=indication → disease/condition only (HIV, melanoma). "
            "worker=id → FDA setid only. "
            "worker=therapeutic_area → broad TA only (oncology). "
            "Never set worker=tradename with query=HIV. "
            "After adverse_effects/clinical_trials with Table placeholders, "
            "fetch paired *_tables (auto-expand may help). Aim for ≥1 trial "
            "per subindication and both ae_reaction + laboratory AE tables."
        ),
        "completeness_gaps": fda_completeness_gaps(evidence),
        "latest_diary": diary[-1].model_dump(mode="json") if diary else None,
        "evidence_tail": compact_evidence_notes(evidence),
    }
    return invoke_schema_with_reader(
        llm,
        PlannerOutput,
        system=load_prompt("fda", "specialist_planner.md"),
        user=json.dumps(payload, indent=2, default=str),
    )
