"""Project one CtgByNctidRow section into a CtgAttrHit."""

from __future__ import annotations

from typing import Any

from model.ctg.ctg_attr_hit import CtgAttrHit
from model.ctg.ctg_attr_name import CtgAttrName
from model.ctg.ctg_by_nctid_row import CtgByNctidRow


def project_attr_hit(row: CtgByNctidRow, attr: CtgAttrName) -> CtgAttrHit:
    """Keep id/setid/nctid plus one section payload."""
    return CtgAttrHit(
        id=row.id,
        setid=row.setid,
        nctid=row.nctid,
        attr=attr,
        value=_section_value(row, attr),
    )


def _section_value(row: CtgByNctidRow, attr: CtgAttrName) -> Any:
    if attr is CtgAttrName.BASIC_INFO:
        return {
            "brief_title": row.brief_title,
            "official_title": row.official_title,
            "enrollment_no": row.enrollment_no,
            "description": row.description,
            "phases": row.phases,
        }
    if attr is CtgAttrName.DEMOGRAPHICS:
        return {
            "arm_groups": row.arm_groups,
            "eligibility_criteria": row.eligibility_criteria,
            "std_ages": row.std_ages,
        }
    if attr is CtgAttrName.CONDITIONS:
        return row.conditions
    if attr is CtgAttrName.LOCATIONS:
        return row.countries
    if attr is CtgAttrName.ADVERSE_EVENTS:
        return {"aes": row.aes, "ae_arms": row.ae_arms}
    if attr is CtgAttrName.OUTCOMES:
        return row.outcomes
    raise ValueError(f"Unsupported CTG attr: {attr}")
