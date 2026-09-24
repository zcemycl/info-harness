"""Expand a projected CT.gov section value into one CtgAttrHit per unit."""

from __future__ import annotations

from typing import Any

from model.ctg.ctg_attr_hit import CtgAttrHit
from model.ctg.ctg_attr_name import CtgAttrName


def expand_ctgov_section_hits(
    nctid: str,
    attr: CtgAttrName,
    value: Any,
) -> list[CtgAttrHit]:
    """Split section payloads so each hit is small enough for full evidence notes."""
    units = _units(attr, value)
    if not units:
        return [CtgAttrHit(id=None, setid=None, nctid=nctid, attr=attr, value=None)]
    return [
        CtgAttrHit(id=None, setid=None, nctid=nctid, attr=attr, value=unit)
        for unit in units
    ]


def _units(attr: CtgAttrName, value: Any) -> list[Any]:
    if value is None:
        return []
    if attr in (CtgAttrName.CONDITIONS, CtgAttrName.LOCATIONS) and isinstance(
        value, list
    ):
        return list(value)
    if attr in (CtgAttrName.OUTCOMES, CtgAttrName.REFERENCES) and isinstance(
        value, list
    ):
        return list(value)
    if attr is CtgAttrName.BASIC_INFO and isinstance(value, dict):
        return [{key: value[key]} for key in value]
    if attr is CtgAttrName.DEMOGRAPHICS and isinstance(value, dict):
        return _demographics_units(value)
    if attr is CtgAttrName.ADVERSE_EVENTS and isinstance(value, dict):
        return _adverse_event_units(value)
    return [value]


def _demographics_units(value: dict[str, Any]) -> list[Any]:
    units: list[Any] = []
    for arm in value.get("arm_groups") or []:
        units.append({"arm_group": arm})
    criteria = value.get("eligibility_criteria")
    if criteria:
        units.append({"eligibility_criteria": criteria})
    ages = value.get("std_ages") or []
    if ages:
        units.append({"std_ages": list(ages)})
    return units


def _adverse_event_units(module: dict[str, Any]) -> list[Any]:
    units: list[Any] = []
    meta_keys = (
        "frequencyThreshold",
        "timeFrame",
        "description",
        "allCauseMortalityComment",
    )
    meta = {k: module[k] for k in meta_keys if k in module and module[k] is not None}
    if meta:
        units.append({"meta": meta})
    for group in module.get("eventGroups") or []:
        units.append({"event_group": group})
    for event in module.get("seriousEvents") or []:
        units.append({"serious_event": event})
    for event in module.get("otherEvents") or []:
        units.append({"other_event": event})
    return units or [module]
