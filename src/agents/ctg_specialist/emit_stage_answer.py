"""Build + persist a PEWE stage answer under the CTG diary tree."""

from __future__ import annotations

from typing import Any

from model.research.agent_answer import (
    AgentAnswer,
    AnswerAudience,
    AnswerStatus,
)
from tools.diary.write_agent_answer import write_agent_answer


def emit_stage_answer(
    *,
    agent: str,
    brief: str,
    answer: str,
    run_id: str,
    loop: int,
    extras: dict[str, Any] | None = None,
    status: AnswerStatus = AnswerStatus.OK,
    audience: AnswerAudience = AnswerAudience.NEXT_AGENT,
) -> AgentAnswer:
    """Write ``data/diary/{run_id}/ctg/loop-{n}/{agent}/answer-*.json``."""
    text = answer.strip() or "(empty stage answer)"
    entry = AgentAnswer(
        agent=agent,
        audience=audience,
        brief=brief,
        answer=text,
        status=status,
        run_id=run_id,
        loop=loop,
        extras=extras or {},
    )
    return write_agent_answer(
        entry,
        name_prefix=f"{run_id}/ctg/loop-{loop}/{agent}",
        filename_stem="answer",
    )
