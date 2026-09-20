"""ICD TA specialist PEWE result pack."""

from __future__ import annotations

from pydantic import BaseModel, Field

from model.research.agent_answer import AgentAnswer
from model.research.diary_entry import DiaryEntry
from model.therapeutic_area.icd_evidence_note import IcdEvidenceNote


class IcdSpecialistResult(BaseModel):
    """Final ICD specialist output: answer, evidence, diary trail."""

    answer: AgentAnswer = Field(description="Human / next-agent facing answer")
    stage_answers: list[AgentAnswer] = Field(default_factory=list)
    evidence: list[IcdEvidenceNote] = Field(default_factory=list)
    diary: list[DiaryEntry] = Field(default_factory=list)
    loops: int = Field(ge=0, description="PEWE loops actually run")
