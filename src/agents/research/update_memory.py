"""Update ResearchMemory after an outer loop from pack + evaluation."""

from __future__ import annotations

from model.research.agent_answer import AnswerStatus
from model.research.research_eval_result import ResearchEvalResult
from model.research.research_memory import (
    ResearchMemory,
    SettledWorkstream,
    TriedIdea,
)
from model.research.research_pack import ResearchPack


def update_research_memory(
    memory: ResearchMemory,
    pack: ResearchPack,
    evaluation: ResearchEvalResult,
    *,
    loop: int,
) -> ResearchMemory:
    """Merge new outcomes and eval lessons into durable outer memory."""
    settled = {item.workstream_id: item for item in memory.settled}
    tried = {item.fingerprint: item for item in memory.tried_ideas}
    failed = list(memory.failed_approaches)
    lessons = list(dict.fromkeys([*memory.lessons, *evaluation.lessons]))
    rejected = list(
        dict.fromkeys([*memory.rejected_directions, *evaluation.reject_directions])
    )
    gaps = list(dict.fromkeys(evaluation.evidence_gaps))

    force = set(evaluation.force_rerun_workstream_ids)
    for outcome in pack.outcomes:
        summary = (outcome.answer.answer or "")[:240]
        tried[outcome.idea_fingerprint] = TriedIdea(
            fingerprint=outcome.idea_fingerprint,
            workstream_id=outcome.workstream_id,
            specialist=outcome.specialist,
            focus=outcome.brief.focus,
            loop=loop,
            status=outcome.status.value,
            summary=summary,
        )
        if outcome.status is AnswerStatus.OK and outcome.workstream_id not in force:
            settled[outcome.workstream_id] = SettledWorkstream(
                workstream_id=outcome.workstream_id,
                specialist=outcome.specialist,
                focus=outcome.brief.focus,
                answer_summary=summary,
                fingerprint=outcome.idea_fingerprint,
            )
        else:
            settled.pop(outcome.workstream_id, None)
            if outcome.error or outcome.status is not AnswerStatus.OK:
                failed.append(
                    f"[{outcome.specialist.value}] {outcome.brief.focus[:120]} "
                    f"→ {outcome.error or outcome.status.value}"
                )

    failed = list(dict.fromkeys(failed))[-40:]
    return ResearchMemory(
        settled=list(settled.values()),
        tried_ideas=list(tried.values()),
        failed_approaches=failed,
        lessons=lessons,
        rejected_directions=rejected,
        open_gaps=gaps,
    )
