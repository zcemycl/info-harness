"""Non-NCT study mention extracted from FDA label text."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field


class StudyMentionKind(StrEnum):
    """Classification of a non-NCT trial identifier in label text."""

    PROTOCOL_ID = "protocol_id"
    ACRONYM = "acronym"
    STUDY_NAME = "study_name"


class StudyMention(BaseModel):
    """One study name / sponsor protocol id from clinical_trials text."""

    raw: str = Field(description="Exact token as found in the source text")
    kind: StudyMentionKind
    aliases: list[str] = Field(
        default_factory=list,
        description="Optional known alternate spellings for this mention",
    )
