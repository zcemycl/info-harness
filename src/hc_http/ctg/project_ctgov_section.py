"""Project one CtgAttrName section from raw CT.gov API v2 study JSON."""

from __future__ import annotations

from typing import Any

from hc_http.ctg.expand_ctgov_section_hits import expand_ctgov_section_hits
from model.ctg.ctg_attr_hit import CtgAttrHit
from model.ctg.ctg_attr_name import CtgAttrName


def project_ctgov_section(raw: dict[str, Any], attr: CtgAttrName) -> CtgAttrHit:
    """Keep nctid plus one section payload shaped like HC CtgAttrHit values."""
    hits = project_ctgov_section_hits(raw, attr)
    return hits[0]


def project_ctgov_section_hits(
    raw: dict[str, Any], attr: CtgAttrName
) -> list[CtgAttrHit]:
    """Project and expand one section into pageable per-unit hits."""
    protocol = raw.get("protocolSection") or {}
    ident = protocol.get("identificationModule") or {}
    nctid = str(ident.get("nctId") or "").strip()
    if not nctid:
        raise RuntimeError("CT.gov study missing nctId")
    return expand_ctgov_section_hits(nctid, attr, _section_value(raw, attr))


def _section_value(raw: dict[str, Any], attr: CtgAttrName) -> Any:
    protocol = raw.get("protocolSection") or {}
    results = raw.get("resultsSection") or {}
    if attr is CtgAttrName.BASIC_INFO:
        return _basic_info(protocol)
    if attr is CtgAttrName.DEMOGRAPHICS:
        return _demographics(protocol)
    if attr is CtgAttrName.CONDITIONS:
        return list((protocol.get("conditionsModule") or {}).get("conditions") or [])
    if attr is CtgAttrName.LOCATIONS:
        return _locations(protocol)
    if attr is CtgAttrName.ADVERSE_EVENTS:
        return results.get("adverseEventsModule")
    if attr is CtgAttrName.OUTCOMES:
        return _outcomes(protocol)
    if attr is CtgAttrName.REFERENCES:
        return _references(protocol)
    raise ValueError(f"Unsupported CT.gov fetch attr: {attr}")


def _basic_info(protocol: dict[str, Any]) -> dict[str, Any]:
    ident = protocol.get("identificationModule") or {}
    desc = protocol.get("descriptionModule") or {}
    design = protocol.get("designModule") or {}
    enrollment = design.get("enrollmentInfo") or {}
    brief = desc.get("briefSummary")
    detailed = desc.get("detailedDescription")
    description = detailed or brief
    return {
        "brief_title": ident.get("briefTitle"),
        "official_title": ident.get("officialTitle"),
        "enrollment_no": enrollment.get("count"),
        "description": description,
        "phases": list(design.get("phases") or []),
    }


def _demographics(protocol: dict[str, Any]) -> dict[str, Any]:
    arms = protocol.get("armsInterventionsModule") or {}
    elig = protocol.get("eligibilityModule") or {}
    return {
        "arm_groups": arms.get("armGroups"),
        "eligibility_criteria": elig.get("eligibilityCriteria"),
        "std_ages": list(elig.get("stdAges") or []),
    }


def _locations(protocol: dict[str, Any]) -> list[str]:
    contacts = protocol.get("contactsLocationsModule") or {}
    countries: list[str] = []
    seen: set[str] = set()
    for loc in contacts.get("locations") or []:
        if not isinstance(loc, dict):
            continue
        country = loc.get("country")
        if isinstance(country, str) and country and country not in seen:
            seen.add(country)
            countries.append(country)
    return countries


def _outcomes(protocol: dict[str, Any]) -> list[dict[str, Any]]:
    module = protocol.get("outcomesModule") or {}
    out: list[dict[str, Any]] = []
    for key, otype in (
        ("primaryOutcomes", "PRIMARY"),
        ("secondaryOutcomes", "SECONDARY"),
        ("otherOutcomes", "OTHER"),
    ):
        for item in module.get(key) or []:
            if not isinstance(item, dict):
                continue
            out.append(
                {
                    "title": item.get("measure"),
                    "type": otype,
                    "arm_groups": None,
                    "timeFrame": item.get("timeFrame"),
                    "measures": [],
                    "description": item.get("description"),
                }
            )
    return out


def _references(protocol: dict[str, Any]) -> list[dict[str, Any]]:
    module = protocol.get("referencesModule") or {}
    refs: list[dict[str, Any]] = []
    for item in module.get("references") or []:
        if not isinstance(item, dict):
            continue
        pmid = item.get("pmid")
        refs.append(
            {
                "pmid": str(pmid) if pmid is not None else None,
                "citation": item.get("citation"),
                "type": item.get("type"),
            }
        )
    for link in module.get("seeAlsoLinks") or []:
        if not isinstance(link, dict):
            continue
        refs.append(
            {
                "pmid": None,
                "citation": link.get("label"),
                "type": "see_also",
                "url": link.get("url"),
            }
        )
    # PMIDs first so truncated evidence summaries keep PubMed ids.
    refs.sort(key=lambda r: (0 if r.get("pmid") else 1))
    return refs
