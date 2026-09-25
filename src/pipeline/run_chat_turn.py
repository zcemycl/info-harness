"""Run one chat turn through the same research pipeline as the CLI."""

from __future__ import annotations

from model.chat.run_event import RunEvent
from model.research.agent_answer import AgentAnswer
from pipeline.run_research import run_research_pipeline
from tools.chat.append_message import append_message
from tools.chat.append_run_event import append_run_event
from tools.chat.put_run_result import put_run_result
from tools.chat.put_run_status import put_run_status
from tools.chat.stage_events import bind_stage_events
from tools.chat.utc_now import utc_now
from tools.cognito.bind_access_token import bind_access_token
from tools.trace_call import trace_info


def run_chat_turn(
    chat_id: str,
    run_id: str,
    brief: str,
    *,
    access_token: str | None = None,
) -> None:
    """Execute PEWE, stream stage events, then store the final answer."""
    if access_token:
        with bind_access_token(access_token):
            _execute(chat_id, run_id, brief)
        return
    _execute(chat_id, run_id, brief)


def _execute(chat_id: str, run_id: str, brief: str) -> None:
    def _on_stage(entry: AgentAnswer) -> None:
        append_run_event(
            RunEvent(
                ts=utc_now(),
                type="stage",
                run_id=run_id,
                chat_id=chat_id,
                loop=entry.loop,
                agent=entry.agent,
                status=entry.status.value,
                summary=_summary(entry.answer),
            )
        )

    try:
        with bind_stage_events(_on_stage):
            result = run_research_pipeline(brief, run_id=run_id)
        answer = result.answer.answer
        put_run_result(chat_id, run_id, answer=answer, loops=result.loops)
        append_message(
            chat_id,
            role="assistant",
            content=answer,
            run_id=run_id,
        )
        append_run_event(
            RunEvent(
                ts=utc_now(),
                type="final",
                run_id=run_id,
                chat_id=chat_id,
                status=result.answer.status.value,
                summary=_summary(answer),
                answer=answer,
            )
        )
        put_run_status(chat_id, run_id, "succeeded")
        trace_info("chat turn complete", run_id=run_id, chat_id=chat_id)
    except Exception as exc:
        message = f"{type(exc).__name__}: {exc}"
        append_run_event(
            RunEvent(
                ts=utc_now(),
                type="error",
                run_id=run_id,
                chat_id=chat_id,
                status="error",
                summary=message,
            )
        )
        put_run_status(chat_id, run_id, "failed", error=message)
        trace_info("chat turn failed", run_id=run_id, error=message)
        raise


def _summary(text: str) -> str:
    collapsed = " ".join(text.split())
    if len(collapsed) <= 240:
        return collapsed
    return collapsed[:237] + "..."
