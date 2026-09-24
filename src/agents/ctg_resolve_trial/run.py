"""Run the CTG resolve_trial worker agent."""

from __future__ import annotations

import uuid

from agents.chat_model import chat_model
from agents.ctg_resolve_trial.tools import resolve_trial_worker_tools
from agents.run_tool_agent import run_tool_agent
from model.research.agent_answer import (
    AgentAnswer,
    AnswerAudience,
    AnswerStatus,
)
from prompt.load_prompt import load_prompt
from tools.diary.write_agent_answer import write_agent_answer
from tools.trace_call import trace_span


def run_ctg_resolve_trial(
    brief: str,
    *,
    max_turns: int = 8,
    run_id: str | None = None,
) -> AgentAnswer:
    """Run the resolve_trial worker; return + persist an answer."""
    rid = run_id or uuid.uuid4().hex[:12]
    with trace_span("worker", "ctg_resolve_trial", max_turns=max_turns):
        result = run_tool_agent(
            model=chat_model(),
            tools=resolve_trial_worker_tools(),
            system=load_prompt("ctg", "resolve_trial_worker.md"),
            user=brief,
            max_turns=max_turns,
        )
        text = result.text.strip()
        status = AnswerStatus.OK if text else AnswerStatus.INCOMPLETE
        return write_agent_answer(
            AgentAnswer(
                agent="ctg_resolve_trial",
                audience=AnswerAudience.BOTH,
                brief=brief,
                answer=text or "(empty worker answer)",
                status=status,
                run_id=rid,
                extras={"tools_called": result.tools_called},
            ),
            name_prefix=f"{rid}/ctg_resolve_trial",
            filename_stem="answer",
        )
