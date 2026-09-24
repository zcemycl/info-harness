"""Search CTG by NCT id; return adverse_events section only."""

from __future__ import annotations

from hc_http.ctg.get_by_nctids import DEFAULT_CACHE_KEY
from model.ctg.ctg_attr_hit import CtgAttrHit
from model.ctg.ctg_attr_name import CtgAttrName
from model.ctg.ctg_attr_page import CtgAttrPage
from model.fda_scrape_versions import DEFAULT_SCRAPE_VERSION
from tools.ctg.search_ctg_nctid.search_attr import search_ctg_nctid_attr


def search_ctg_nctid_adverse_events(
    nctid: str,
    *,
    version: str = DEFAULT_SCRAPE_VERSION,
    cache_key: str = DEFAULT_CACHE_KEY,
    offset: int = 0,
    limit: int = 5,
) -> CtgAttrPage[CtgAttrHit]:
    """Search by NCT id; return adverse_events page."""
    return search_ctg_nctid_attr(
        CtgAttrName.ADVERSE_EVENTS,
        nctid,
        version=version,
        cache_key=cache_key,
        offset=offset,
        limit=limit,
    )
