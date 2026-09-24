"""One spawned specialist outcome inside a research pack."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from model.research.agent_answer import AgentAnswer, AnswerStatus
from model.research.specialist_brief import SpecialistBrief
from model.research.specialist_kind import SpecialistKind


class ResearchOutcome(BaseModel):
    """Result of one specialist spawn (success or failure wrapper)."""

    workstream_id: str = Field(description="Stable workstream key used for merge/lock")
    specialist: SpecialistKind
    brief: SpecialistBrief
    idea_fingerprint: str = Field(
        description="Normalized fingerprint of the idea that was tried"
    )
    answer: AgentAnswer
    status: AnswerStatus = Field(default=AnswerStatus.OK)
    error: str | None = Field(default=None)
    specialist_result: dict[str, Any] | None = Field(
        default=None,
        description="Raw specialist result dump when available",
    )
