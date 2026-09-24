"""PubMed specialist PEWE result pack."""

from __future__ import annotations

from pydantic import BaseModel, Field

from model.pubmed.pubmed_evidence_note import PubmedEvidenceNote
from model.research.agent_answer import AgentAnswer
from model.research.diary_entry import DiaryEntry


class PubmedSpecialistResult(BaseModel):
    """Final PubMed specialist output: answer, evidence, diary trail."""

    answer: AgentAnswer = Field(description="Human / next-agent facing answer")
    stage_answers: list[AgentAnswer] = Field(default_factory=list)
    evidence: list[PubmedEvidenceNote] = Field(default_factory=list)
    diary: list[DiaryEntry] = Field(default_factory=list)
    loops: int = Field(ge=0, description="PEWE loops actually run")
