"""Classify FDA adverse-effect table captions into reaction vs laboratory."""

from __future__ import annotations

import re

from model.fda.ae_table_kind import AeTableKind

_LAB_RE = re.compile(r"laboratory\s+abnormalit", re.IGNORECASE)
_AE_RE = re.compile(
    r"adverse\s+reaction|treatment-emergent.*adverse|all\s+causality.*adverse",
    re.IGNORECASE,
)


def classify_ae_table_kind(caption: str | None) -> AeTableKind:
    """Return ae_reaction / laboratory / other from a table caption."""
    text = (caption or "").strip()
    if not text:
        return AeTableKind.OTHER
    if _LAB_RE.search(text):
        return AeTableKind.LABORATORY
    if _AE_RE.search(text):
        return AeTableKind.AE_REACTION
    return AeTableKind.OTHER
