"""FDA label specialist result returned by the PEWE loop."""

from __future__ import annotations

from pydantic import BaseModel, Field

from model.research.agent_answer import AgentAnswer
from model.research.diary_entry import DiaryEntry
from model.research.evidence_note import EvidenceNote


class FdaSpecialistResult(BaseModel):
    """Final specialist output: answers, evidence, and diary trail."""

    answer: AgentAnswer = Field(
        description="Human / outer-agent facing answer from synthesize"
    )
    stage_answers: list[AgentAnswer] = Field(
        default_factory=list,
        description="Per-stage answers for the next PEWE stage",
    )
    evidence: list[EvidenceNote] = Field(default_factory=list)
    diary: list[DiaryEntry] = Field(default_factory=list)
    loops: int = Field(ge=0, description="PEWE loops actually run")
