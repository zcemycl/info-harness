"""Universal agent answer for humans or the next agent in the chain."""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class AnswerAudience(StrEnum):
    """Who the answer is primarily written for."""

    HUMAN = "human"
    NEXT_AGENT = "next_agent"
    BOTH = "both"


class AnswerStatus(StrEnum):
    """Outcome status attached to an agent answer."""

    OK = "ok"
    INCOMPLETE = "incomplete"
    ERROR = "error"


class AgentAnswer(BaseModel):
    """Every agent (worker / stage / specialist / outer) returns this."""

    agent: str = Field(description="Agent or stage name that produced the answer")
    audience: AnswerAudience = Field(
        default=AnswerAudience.BOTH,
        description="human | next_agent | both",
    )
    brief: str = Field(default="", description="Input brief or task this answers")
    answer: str = Field(
        description="Natural-language answer for a human or the next agent"
    )
    status: AnswerStatus = Field(default=AnswerStatus.OK)
    run_id: str | None = Field(default=None, description="Shared run id when nested")
    loop: int | None = Field(default=None, ge=1, description="Loop index when nested")
    path: str | None = Field(
        default=None, description="Diary-relative path if persisted"
    )
    extras: dict[str, Any] = Field(
        default_factory=dict,
        description="Structured payload for the next agent (plans, ids, etc.)",
    )
