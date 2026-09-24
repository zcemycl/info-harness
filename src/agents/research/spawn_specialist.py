"""Spawn one specialist pipeline from a SpecialistBrief (sync body)."""

from __future__ import annotations

from typing import Any

from agents.research.fingerprint_idea import fingerprint_brief
from model.research.agent_answer import (
    AgentAnswer,
    AnswerAudience,
    AnswerStatus,
)
from model.research.research_outcome import ResearchOutcome
from model.research.specialist_brief import SpecialistBrief
from model.research.specialist_kind import SpecialistKind
from pipeline.run_ctg_specialist import run_ctg_specialist_pipeline
from pipeline.run_fda_label_specialist import run_fda_label_specialist_pipeline
from pipeline.run_icd_ta_specialist import run_icd_ta_specialist_pipeline


def spawn_specialist_sync(
    brief: SpecialistBrief,
    *,
    run_id: str,
    specialist_max_loops: int | None = None,
) -> ResearchOutcome:
    """Run the matching specialist pipeline; wrap failures as ERROR outcomes."""
    wid = brief.workstream_id or f"{brief.specialist.value}-unknown"
    focus = _compose_focus(brief)
    child_run_id = f"{run_id}/research/{wid}"
    fp = fingerprint_brief(brief)
    try:
        result = _dispatch(brief.specialist, focus, specialist_max_loops, child_run_id)
        answer = result.answer
        dump = result.model_dump(mode="json")
        return ResearchOutcome(
            workstream_id=wid,
            specialist=brief.specialist,
            brief=brief,
            idea_fingerprint=fp,
            answer=answer,
            status=answer.status,
            specialist_result=dump,
        )
    except Exception as exc:  # noqa: BLE001 — outer loop must not die on one spawn
        return ResearchOutcome(
            workstream_id=wid,
            specialist=brief.specialist,
            brief=brief,
            idea_fingerprint=fp,
            answer=AgentAnswer(
                agent=f"{brief.specialist.value}_specialist",
                audience=AnswerAudience.NEXT_AGENT,
                brief=focus,
                answer=f"Specialist failed: {exc}",
                status=AnswerStatus.ERROR,
                run_id=child_run_id,
            ),
            status=AnswerStatus.ERROR,
            error=str(exc),
        )


def _compose_focus(brief: SpecialistBrief) -> str:
    if not brief.seed_queries:
        return brief.focus
    seeds = ", ".join(brief.seed_queries)
    return f"{brief.focus}\n\nSeed queries: {seeds}"


def _dispatch(
    kind: SpecialistKind,
    focus: str,
    max_loops: int | None,
    run_id: str,
) -> Any:
    if kind is SpecialistKind.FDA_LABEL:
        return run_fda_label_specialist_pipeline(
            focus, max_loops=max_loops, run_id=run_id
        )
    if kind is SpecialistKind.CTG:
        return run_ctg_specialist_pipeline(focus, max_loops=max_loops, run_id=run_id)
    if kind is SpecialistKind.ICD_TA:
        return run_icd_ta_specialist_pipeline(focus, max_loops=max_loops, run_id=run_id)
    raise ValueError(f"Unsupported specialist: {kind}")
