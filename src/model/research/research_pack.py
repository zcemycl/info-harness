"""Merged pack of research specialist outcomes for one or more loops."""

from __future__ import annotations

from pydantic import BaseModel, Field

from model.research.research_outcome import ResearchOutcome


class ResearchPack(BaseModel):
    """All workstream outcomes visible to writer/evaluator."""

    outcomes: list[ResearchOutcome] = Field(default_factory=list)
