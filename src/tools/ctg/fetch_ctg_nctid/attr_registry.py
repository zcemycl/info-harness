"""Map CtgAttrName → live NCT-id fetch callables."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from model.ctg.ctg_attr_name import CtgAttrName
from tools.ctg.fetch_ctg_nctid import (
    adverse_events,
    basic_info,
    conditions,
    demographics,
    locations,
    outcomes,
    references,
)

NctidFetch = Callable[..., Any]

NCTID_ATTR_FETCH: dict[CtgAttrName, NctidFetch] = {
    CtgAttrName.BASIC_INFO: basic_info.fetch_ctg_nctid_basic_info,
    CtgAttrName.DEMOGRAPHICS: demographics.fetch_ctg_nctid_demographics,
    CtgAttrName.CONDITIONS: conditions.fetch_ctg_nctid_conditions,
    CtgAttrName.LOCATIONS: locations.fetch_ctg_nctid_locations,
    CtgAttrName.ADVERSE_EVENTS: adverse_events.fetch_ctg_nctid_adverse_events,
    CtgAttrName.OUTCOMES: outcomes.fetch_ctg_nctid_outcomes,
    CtgAttrName.REFERENCES: references.fetch_ctg_nctid_references,
}
