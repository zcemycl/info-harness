"""Fingerprint a research idea so identical plans are not re-tried."""

from __future__ import annotations

import hashlib
import re

from model.research.specialist_brief import SpecialistBrief
from model.research.specialist_kind import SpecialistKind

_WS = re.compile(r"\s+")


def fingerprint_idea(
    specialist: SpecialistKind,
    focus: str,
    seed_queries: list[str] | None = None,
) -> str:
    """Return a stable short hash for specialist+focus+seeds."""
    seeds = sorted(_norm(s) for s in (seed_queries or []) if s.strip())
    payload = "|".join([specialist.value, _norm(focus), *seeds])
    return hashlib.sha1(payload.encode("utf-8")).hexdigest()[:16]


def fingerprint_brief(brief: SpecialistBrief) -> str:
    """Fingerprint a SpecialistBrief."""
    return fingerprint_idea(brief.specialist, brief.focus, brief.seed_queries)


def _norm(text: str) -> str:
    return _WS.sub(" ", text.strip().lower())
