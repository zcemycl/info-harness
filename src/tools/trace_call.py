"""Indented loguru tracing for agent / worker / tool / loop calls."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar, Token
from typing import Any

from loguru import logger

_depth: ContextVar[int] = ContextVar("trace_call_depth", default=0)
_agent: ContextVar[str] = ContextVar("trace_agent", default="")
_loop: ContextVar[int | None] = ContextVar("trace_loop", default=None)

_AGENT_SCOPE = {
    "research": ("outer", "research"),
    "fda_label_specialist": ("inner", "fda"),
    "ctg_specialist": ("inner", "ctg"),
    "pubmed_specialist": ("inner", "pubmed"),
    "icd_ta_specialist": ("inner", "icd"),
}
_STAGE_START = {
    "planner": "Planner running.",
    "executor": "Executor running; spawning is in progress and this loop stays open.",
    "writer": "Writer running; spawned work converges here.",
    "evaluator": "Evaluator running.",
}


def trace_info(message: str, **fields: Any) -> None:
    """Log one line at the current nest depth."""
    logger.info(_format(message, fields))


@contextmanager
def trace_span(kind: str, name: str, **fields: Any) -> Iterator[None]:
    """Enter/leave a nested call; children indent two spaces further."""
    depth = _depth.get()
    trace_info(f"→ {kind} {name}", **fields)
    depth_token = _depth.set(depth + 1)
    agent_token = _agent.set(name) if kind == "agent" and name in _AGENT_SCOPE else None
    loop_num = name.split("/")[0]
    loop_token = (
        _loop.set(int(loop_num)) if kind == "loop" and loop_num.isdigit() else None
    )
    if kind == "stage":
        _emit_stage_start(name)
    try:
        yield
    except Exception as exc:
        logger.opt(exception=False).error(
            _format(f"✗ {kind} {name}", {"error": f"{type(exc).__name__}: {exc}"})
        )
        raise
    finally:
        _reset(_loop, loop_token)
        _reset(_agent, agent_token)
        _depth.reset(depth_token)
        logger.info(_format(f"finished {kind} {name}", {}))


def _emit_stage_start(name: str) -> None:
    mapped = _AGENT_SCOPE.get(_agent.get())
    summary = _STAGE_START.get(name)
    if mapped is None or summary is None:
        return
    from tools.chat.stage_events import notify_stage_phase

    tier, domain = mapped
    notify_stage_phase(
        tier=tier,
        domain=domain,
        stage=name,
        loop=_loop.get(),
        phase="start",
        summary=summary,
    )


def _reset(var: ContextVar[Any], token: Token[Any] | None) -> None:
    if token is not None:
        var.reset(token)


def _format(message: str, fields: dict[str, Any]) -> str:
    indent = "  " * _depth.get()
    extras = " ".join(
        f"{key}={value!r}" for key, value in fields.items() if value is not None
    )
    if extras:
        return f"{indent}{message}  {extras}"
    return f"{indent}{message}"
