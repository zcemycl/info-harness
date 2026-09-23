"""Search by setid and project one fixed FdaLabel attribute."""

from __future__ import annotations

from hc_http.fda.search_by_id import run_search_fdalabel_by_id
from model.fda.fda_attr_name import FdaAttrName
from model.fda.fda_label_attr_hit import FdaLabelAttrHit
from model.fda.fda_label_attr_page import FdaLabelAttrPage
from model.fda_scrape_versions import FdaScrapeVersions
from tools.fda.project_attr_hit import project_attr_hit
from tools.trace_call import trace_info, trace_span
from tools.wrap_attr_page import wrap_attr_page


def search_fdalabel_id_attr(
    attr: FdaAttrName,
    setid: str,
    *,
    versions: FdaScrapeVersions | None = None,
    maxn: int = 30,
    offset: int = 0,
    limit: int = 5,
) -> FdaLabelAttrPage[FdaLabelAttrHit]:
    """Search by setid; return id/setid/tradename/<attr> page."""
    with trace_span(
        "tool",
        f"search_fdalabel_id_{attr.value}",
        setid=setid,
        offset=offset,
        limit=limit,
        maxn=maxn,
    ):
        labels = run_search_fdalabel_by_id(
            [setid], versions=versions, maxn=maxn, offset=offset, limit=limit
        )
        items = [project_attr_hit(label, attr) for label in labels]
        page = wrap_attr_page(items, offset=offset, limit=limit)
        trace_info("page", items=len(page.items), next_offset=page.next_offset)
        return page
