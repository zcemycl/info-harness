"""Optional listener for diary stage writes during a chat run."""

from __future__ import annotations

from collections.abc import Callable, Iterator
from contextlib import contextmanager
from contextvars import ContextVar

from loguru import logger

from model.research.agent_answer import AgentAnswer

_listener: ContextVar[Callable[[AgentAnswer], None] | None] = ContextVar(
    "chat_stage_listener",
    default=None,
)
_phase: ContextVar[Callable[..., None] | None] = ContextVar(
    "chat_stage_phase",
    default=None,
)


def notify_stage(entry: AgentAnswer) -> None:
    """Forward a persisted stage answer. No listener means CLI no-op."""
    callback = _listener.get()
    if callback is None:
        return
    try:
        callback(entry)
    except Exception:
        logger.exception("stage event listener failed")


def notify_stage_phase(
    *,
    tier: str,
    domain: str,
    stage: str,
    loop: int | None,
    phase: str,
    summary: str,
) -> None:
    """Forward a stage start or end. No listener means CLI no-op."""
    callback = _phase.get()
    if callback is None:
        return
    try:
        callback(
            tier=tier,
            domain=domain,
            stage=stage,
            loop=loop,
            phase=phase,
            summary=summary,
        )
    except Exception:
        logger.exception("stage phase listener failed")


@contextmanager
def bind_stage_events(
    callback: Callable[[AgentAnswer], None],
    *,
    on_phase: Callable[..., None] | None = None,
) -> Iterator[None]:
    """Bind stage listeners for nested specialist threads in this context."""
    token = _listener.set(callback)
    phase_token = _phase.set(on_phase)
    try:
        yield
    finally:
        _phase.reset(phase_token)
        _listener.reset(token)
