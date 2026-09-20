"""Search FDA labels by tradename; return adverse-effects hits only."""

from __future__ import annotations

from hc_http.fda.search_by_tradename import run_search_fdalabel_tradename
from model.fda.fda_label_adverse_effects_hit import FdaLabelAdverseEffectsHit
from model.fda.fda_label_attr_page import FdaLabelAttrPage
from model.fda_scrape_versions import FdaScrapeVersions
from tools.fda.project_adverse_effects_hit import project_adverse_effects_hit
from tools.fda.wrap_attr_page import wrap_attr_page
from tools.trace_call import trace_info, trace_span


def search_fdalabel_tradename_adverse_effects(
    tradename: str,
    *,
    versions: FdaScrapeVersions | None = None,
    maxn: int = 30,
    offset: int = 0,
    limit: int = 5,
) -> FdaLabelAttrPage[FdaLabelAdverseEffectsHit]:
    """Search by tradename; return id/setid/tradename/adverse_effects page."""
    with trace_span(
        "tool",
        "search_fdalabel_tradename_adverse_effects",
        tradename=tradename,
        offset=offset,
        limit=limit,
        maxn=maxn,
    ):
        labels = run_search_fdalabel_tradename(
            tradename, versions=versions, maxn=maxn, offset=offset, limit=limit
        )
        items = [project_adverse_effects_hit(label) for label in labels]
        page = wrap_attr_page(items, offset=offset, limit=limit)
        trace_info("page", items=len(page.items), next_offset=page.next_offset)
        return page
