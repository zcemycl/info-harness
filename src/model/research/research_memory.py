"""Cross-loop memory so the research planner does not forget settled work."""

from __future__ import annotations

from pydantic import BaseModel, Field

from model.research.specialist_kind import SpecialistKind


class TriedIdea(BaseModel):
    """One idea the outer loop already attempted."""

    fingerprint: str
    workstream_id: str
    specialist: SpecialistKind
    focus: str
    loop: int = Field(ge=1)
    status: str = Field(description="ok | incomplete | error")
    summary: str = Field(default="", description="Short outcome summary")


class SettledWorkstream(BaseModel):
    """A workstream whose answer is good enough to lock."""

    workstream_id: str
    specialist: SpecialistKind
    focus: str
    answer_summary: str
    fingerprint: str


class ResearchMemory(BaseModel):
    """Accumulated outer-loop memory (improves on FDE prior_pack-only recall)."""

    settled: list[SettledWorkstream] = Field(default_factory=list)
    tried_ideas: list[TriedIdea] = Field(default_factory=list)
    failed_approaches: list[str] = Field(
        default_factory=list,
        description="Human-readable failed approaches to avoid repeating",
    )
    lessons: list[str] = Field(
        default_factory=list,
        description="Evaluator/planner lessons carried across loops",
    )
    rejected_directions: list[str] = Field(
        default_factory=list,
        description="General directions that did not help",
    )
    open_gaps: list[str] = Field(
        default_factory=list,
        description="Still-open evidence gaps",
    )

    def settled_ids(self) -> set[str]:
        """Return locked workstream ids."""
        return {item.workstream_id for item in self.settled}

    def tried_fingerprints(self) -> set[str]:
        """Return fingerprints of ideas already attempted."""
        return {item.fingerprint for item in self.tried_ideas}
