"""Search FDA labels by indication text; return adverse-effects hits only."""

from __future__ import annotations

from hc_http.fda._cache_key import DEFAULT_CACHE_KEY
from hc_http.fda.search_by_indication import (
    DEFAULT_SORT_BY,
    run_search_fdalabel_indication,
)
from model.fda.fda_label_adverse_effects_hit import FdaLabelAdverseEffectsHit
from model.fda.fda_label_attr_page import FdaLabelAttrPage
from model.fda_scrape_versions import FdaScrapeVersions
from tools.fda.project_adverse_effects_hit import project_adverse_effects_hit
from tools.fda.wrap_attr_page import wrap_attr_page
from tools.trace_call import trace_info, trace_span


def search_fdalabel_indication_adverse_effects(
    indication: str,
    *,
    versions: FdaScrapeVersions | None = None,
    maxn: int = 30,
    offset: int = 0,
    limit: int = 5,
    sort_by: str = DEFAULT_SORT_BY,
    cache_key: str = DEFAULT_CACHE_KEY,
) -> FdaLabelAttrPage[FdaLabelAdverseEffectsHit]:
    """Search by indication; return id/setid/tradename/adverse_effects page."""
    with trace_span(
        "tool",
        "search_fdalabel_indication_adverse_effects",
        indication=indication,
        offset=offset,
        limit=limit,
        maxn=maxn,
    ):
        labels = run_search_fdalabel_indication(
            indication,
            versions=versions,
            maxn=maxn,
            offset=offset,
            limit=limit,
            sort_by=sort_by,
            cache_key=cache_key,
        )
        items = [project_adverse_effects_hit(label) for label in labels]
        page = wrap_attr_page(items, offset=offset, limit=limit)
        trace_info("page", items=len(page.items), next_offset=page.next_offset)
        return page
