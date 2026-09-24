"""Fixed CTG study section names for attr-scoped tools (not free-form)."""

from __future__ import annotations

from enum import StrEnum


class CtgAttrName(StrEnum):
    """Study sections for CTG search (HC) and fetch (live CT.gov) tools."""

    BASIC_INFO = "basic_info"
    DEMOGRAPHICS = "demographics"
    CONDITIONS = "conditions"
    LOCATIONS = "locations"
    ADVERSE_EVENTS = "adverse_events"
    OUTCOMES = "outcomes"
    REFERENCES = "references"


# HC search_ctg_nctid_* supports these; references is fetch-only.
HC_CTG_ATTRS: frozenset[CtgAttrName] = frozenset(
    {
        CtgAttrName.BASIC_INFO,
        CtgAttrName.DEMOGRAPHICS,
        CtgAttrName.CONDITIONS,
        CtgAttrName.LOCATIONS,
        CtgAttrName.ADVERSE_EVENTS,
        CtgAttrName.OUTCOMES,
    }
)

FETCH_CTG_ATTRS: frozenset[CtgAttrName] = HC_CTG_ATTRS | {CtgAttrName.REFERENCES}
