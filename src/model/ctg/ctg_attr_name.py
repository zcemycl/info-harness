"""Fixed CTG study section names for attr-scoped tools (not free-form)."""

from __future__ import annotations

from enum import StrEnum


class CtgAttrName(StrEnum):
    """Every CtgByNctidRow section exposed as its own tool."""

    BASIC_INFO = "basic_info"
    DEMOGRAPHICS = "demographics"
    CONDITIONS = "conditions"
    LOCATIONS = "locations"
    ADVERSE_EVENTS = "adverse_events"
    OUTCOMES = "outcomes"
