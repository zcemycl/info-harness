"""Map CtgAttrName → NCT-id attr search callables."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from model.ctg.ctg_attr_name import CtgAttrName
from tools.ctg.search_ctg_nctid import (
    adverse_events,
    basic_info,
    conditions,
    demographics,
    locations,
    outcomes,
)

NctidSearch = Callable[..., Any]

NCTID_ATTR_SEARCH: dict[CtgAttrName, NctidSearch] = {
    CtgAttrName.BASIC_INFO: basic_info.search_ctg_nctid_basic_info,
    CtgAttrName.DEMOGRAPHICS: demographics.search_ctg_nctid_demographics,
    CtgAttrName.CONDITIONS: conditions.search_ctg_nctid_conditions,
    CtgAttrName.LOCATIONS: locations.search_ctg_nctid_locations,
    CtgAttrName.ADVERSE_EVENTS: adverse_events.search_ctg_nctid_adverse_events,
    CtgAttrName.OUTCOMES: outcomes.search_ctg_nctid_outcomes,
}
