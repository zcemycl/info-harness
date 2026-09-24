"""Fetch live CT.gov by NCT id and project one fixed study section."""

from __future__ import annotations

from hc_http.ctg.get_ctgov_study_raw import run_get_ctgov_study_raw
from hc_http.ctg.project_ctgov_section import project_ctgov_section_hits
from model.ctg.ctg_attr_hit import CtgAttrHit
from model.ctg.ctg_attr_name import CtgAttrName
from model.ctg.ctg_attr_page import CtgAttrPage
from tools.trace_call import trace_info, trace_span
from tools.wrap_attr_page import wrap_attr_page


def fetch_ctg_nctid_attr(
    attr: CtgAttrName,
    nctid: str,
    *,
    offset: int = 0,
    limit: int = 5,
) -> CtgAttrPage[CtgAttrHit]:
    """Fetch live study by NCT id; return expanded nctid/<attr> page."""
    with trace_span(
        "tool",
        f"fetch_ctg_nctid_{attr.value}",
        nctid=nctid,
        offset=offset,
        limit=limit,
    ):
        raw = run_get_ctgov_study_raw(nctid)
        projected = project_ctgov_section_hits(raw, attr)
        page_items = projected[offset : offset + limit]
        page = wrap_attr_page(page_items, offset=offset, limit=limit)
        trace_info(
            "page",
            items=len(page.items),
            total=len(projected),
            next_offset=page.next_offset,
        )
        return page
