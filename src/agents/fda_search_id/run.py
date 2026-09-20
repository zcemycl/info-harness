"""Run the FDA setid search worker agent."""

from __future__ import annotations

import uuid

from agents.chat_model import chat_model
from agents.fda_search_id.tools import id_worker_tools
from agents.run_tool_agent import run_tool_agent
from model.research.agent_answer import (
    AgentAnswer,
    AnswerAudience,
    AnswerStatus,
)
from prompt.load_prompt import load_prompt
from tools.diary.write_agent_answer import write_agent_answer
from tools.trace_call import trace_span


def run_fda_search_id(
    brief: str,
    *,
    max_turns: int = 8,
    run_id: str | None = None,
) -> AgentAnswer:
    """Run the setid worker; return + persist an answer for human/next agent."""
    rid = run_id or uuid.uuid4().hex[:12]
    with trace_span("worker", "fda_search_id", max_turns=max_turns):
        text = run_tool_agent(
            model=chat_model(),
            tools=id_worker_tools(),
            system=load_prompt("fda", "search_id_worker.md"),
            user=brief,
            max_turns=max_turns,
        ).strip()
        status = AnswerStatus.OK if text else AnswerStatus.INCOMPLETE
        return write_agent_answer(
            AgentAnswer(
                agent="fda_search_id",
                audience=AnswerAudience.BOTH,
                brief=brief,
                answer=text or "(empty worker answer)",
                status=status,
                run_id=rid,
            ),
            name_prefix=f"{rid}/fda_search_id",
            filename_stem="answer",
        )
