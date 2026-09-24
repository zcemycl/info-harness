"""Adverse-effect table kind from caption text."""

from __future__ import annotations

from enum import StrEnum


class AeTableKind(StrEnum):
    """Coarse kind for FDA adverse_effect_tables captions."""

    AE_REACTION = "ae_reaction"
    LABORATORY = "laboratory"
    OTHER = "other"
