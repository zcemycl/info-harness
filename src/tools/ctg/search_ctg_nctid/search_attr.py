"""Search by NCT id and project one fixed CtgByNctidRow section."""

from __future__ import annotations

from hc_http.ctg.get_by_nctids import DEFAULT_CACHE_KEY
from model.ctg.ctg_attr_hit import CtgAttrHit
from model.ctg.ctg_attr_name import CtgAttrName
from model.ctg.ctg_attr_page import CtgAttrPage
from model.fda_scrape_versions import DEFAULT_SCRAPE_VERSION
from tools.ctg.get_ctg_by_nctids import get_ctg_by_nctids
from tools.ctg.project_attr_hit import project_attr_hit
from tools.ctg.wrap_attr_page import wrap_attr_page
from tools.trace_call import trace_info, trace_span


def search_ctg_nctid_attr(
    attr: CtgAttrName,
    nctid: str,
    *,
    version: str = DEFAULT_SCRAPE_VERSION,
    cache_key: str = DEFAULT_CACHE_KEY,
    offset: int = 0,
    limit: int = 5,
) -> CtgAttrPage[CtgAttrHit]:
    """Fetch by NCT id; return id/setid/nctid/<attr> page."""
    with trace_span(
        "tool",
        f"search_ctg_nctid_{attr.value}",
        nctid=nctid,
        offset=offset,
        limit=limit,
    ):
        rows = get_ctg_by_nctids([nctid], version=version, cache_key=cache_key)
        projected = [project_attr_hit(row, attr) for row in rows]
        page_items = projected[offset : offset + limit]
        page = wrap_attr_page(page_items, offset=offset, limit=limit)
        trace_info("page", items=len(page.items), next_offset=page.next_offset)
        return page
