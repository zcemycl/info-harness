"""Search by therapeutic area and project one fixed FdaLabel attribute."""

from __future__ import annotations

from hc_http.fda.search_by_therapeutic_area import (
    DEFAULT_SORT_BY,
    run_search_fdalabel_by_therapeutic_area,
)
from model.fda.fda_attr_name import FdaAttrName
from model.fda.fda_label_attr_hit import FdaLabelAttrHit
from model.fda.fda_label_attr_page import FdaLabelAttrPage
from model.fda_scrape_versions import FdaScrapeVersions
from tools.fda.project_attr_hit import project_attr_hit
from tools.trace_call import trace_info, trace_span
from tools.wrap_attr_page import wrap_attr_page


def search_fdalabel_therapeutic_area_attr(
    attr: FdaAttrName,
    ta_description: str,
    *,
    versions: FdaScrapeVersions | None = None,
    maxn: int = 30,
    offset: int = 0,
    limit: int = 5,
    sort_by: str = DEFAULT_SORT_BY,
) -> FdaLabelAttrPage[FdaLabelAttrHit]:
    """Search by therapeutic area; return id/setid/tradename/<attr> page."""
    with trace_span(
        "tool",
        f"search_fdalabel_therapeutic_area_{attr.value}",
        ta_description=ta_description,
        offset=offset,
        limit=limit,
        maxn=maxn,
    ):
        labels = run_search_fdalabel_by_therapeutic_area(
            ta_description,
            versions=versions,
            maxn=maxn,
            offset=offset,
            limit=limit,
            sort_by=sort_by,
        )
        items = [project_attr_hit(label, attr) for label in labels]
        page = wrap_attr_page(items, offset=offset, limit=limit)
        trace_info("page", items=len(page.items), next_offset=page.next_offset)
        return page
