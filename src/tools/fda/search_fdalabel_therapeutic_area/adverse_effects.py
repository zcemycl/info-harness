"""Search FDA labels by therapeutic area; return adverse_effects hits only."""

from __future__ import annotations

from hc_http.fda.search_by_therapeutic_area import DEFAULT_SORT_BY
from model.fda.fda_attr_name import FdaAttrName
from model.fda.fda_label_attr_hit import FdaLabelAttrHit
from model.fda.fda_label_attr_page import FdaLabelAttrPage
from model.fda_scrape_versions import FdaScrapeVersions
from tools.fda.search_fdalabel_therapeutic_area.search_attr import (
    search_fdalabel_therapeutic_area_attr,
)


def search_fdalabel_therapeutic_area_adverse_effects(
    ta_description: str,
    *,
    versions: FdaScrapeVersions | None = None,
    maxn: int = 30,
    offset: int = 0,
    limit: int = 5,
    sort_by: str = DEFAULT_SORT_BY,
) -> FdaLabelAttrPage[FdaLabelAttrHit]:
    """Search by therapeutic area; return adverse_effects page."""
    return search_fdalabel_therapeutic_area_attr(
        FdaAttrName.ADVERSE_EFFECTS,
        ta_description,
        versions=versions,
        maxn=maxn,
        offset=offset,
        limit=limit,
        sort_by=sort_by,
    )
