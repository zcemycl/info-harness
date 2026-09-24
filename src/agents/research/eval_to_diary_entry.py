"""Convert ResearchEvalResult into a diary DiaryEntry for persistence."""

from __future__ import annotations

from model.research.diary_entry import DiaryEntry
from model.research.research_eval_result import ResearchEvalResult


def eval_to_diary_entry(evaluation: ResearchEvalResult) -> DiaryEntry:
    """Map outer eval fields onto the shared DiaryEntry schema."""
    return DiaryEntry(
        loop=evaluation.loop,
        observations=list(evaluation.observations),
        successful_actions=list(evaluation.successful_actions),
        failures=list(evaluation.failures),
        evidence_gaps=list(evaluation.evidence_gaps),
        contradictions=list(evaluation.contradictions),
        lessons=list(evaluation.lessons),
        recommended_next_actions=list(evaluation.recommended_next_actions),
        decision=evaluation.decision,
    )
