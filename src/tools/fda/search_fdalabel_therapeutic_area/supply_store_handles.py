"""Search FDA labels by therapeutic area; return supply_store_handles hits only."""

from __future__ import annotations

from hc_http.fda.search_by_therapeutic_area import DEFAULT_SORT_BY
from model.fda.fda_attr_name import FdaAttrName
from model.fda.fda_label_attr_hit import FdaLabelAttrHit
from model.fda.fda_label_attr_page import FdaLabelAttrPage
from model.fda_scrape_versions import FdaScrapeVersions
from tools.fda.search_fdalabel_therapeutic_area.search_attr import (
    search_fdalabel_therapeutic_area_attr,
)


def search_fdalabel_therapeutic_area_supply_store_handles(
    ta_description: str,
    *,
    versions: FdaScrapeVersions | None = None,
    maxn: int = 30,
    offset: int = 0,
    limit: int = 5,
    sort_by: str = DEFAULT_SORT_BY,
) -> FdaLabelAttrPage[FdaLabelAttrHit]:
    """Search by therapeutic area; return supply_store_handles page."""
    return search_fdalabel_therapeutic_area_attr(
        FdaAttrName.SUPPLY_STORE_HANDLES,
        ta_description,
        versions=versions,
        maxn=maxn,
        offset=offset,
        limit=limit,
        sort_by=sort_by,
    )
