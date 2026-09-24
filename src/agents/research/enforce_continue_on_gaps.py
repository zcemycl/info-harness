"""Force continue when critical workstreams failed and evaluator said complete."""

from __future__ import annotations

from model.research.agent_answer import AnswerStatus
from model.research.diary_entry import DiaryDecision
from model.research.research_eval_result import ResearchEvalResult
from model.research.research_pack import ResearchPack


def enforce_continue_on_gaps(
    evaluation: ResearchEvalResult,
    pack: ResearchPack,
) -> ResearchEvalResult:
    """Cannot complete when every outcome is error/incomplete."""
    if evaluation.decision is not DiaryDecision.COMPLETE:
        return evaluation
    if not pack.outcomes:
        return evaluation.model_copy(
            update={
                "decision": DiaryDecision.REPLAN,
                "failures": [
                    *evaluation.failures,
                    "No workstreams produced outcomes; cannot complete.",
                ],
                "recommended_next_actions": [
                    *evaluation.recommended_next_actions,
                    "Plan at least one specialist workstream.",
                ],
            }
        )
    bad = [
        o
        for o in pack.outcomes
        if o.status in (AnswerStatus.ERROR, AnswerStatus.INCOMPLETE) or o.error
    ]
    if len(bad) == len(pack.outcomes):
        return evaluation.model_copy(
            update={
                "decision": DiaryDecision.CONTINUE,
                "failures": [
                    *evaluation.failures,
                    "All workstreams incomplete/error; forcing continue.",
                ],
                "evidence_gaps": list(
                    dict.fromkeys(
                        [
                            *evaluation.evidence_gaps,
                            *[o.error or o.status.value for o in bad],
                        ]
                    )
                ),
            }
        )
    return evaluation
