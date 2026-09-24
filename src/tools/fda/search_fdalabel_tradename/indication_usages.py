"""Search FDA labels by tradename; return indication_usages hits only."""

from __future__ import annotations

from model.fda.fda_attr_name import FdaAttrName
from model.fda.fda_label_attr_hit import FdaLabelAttrHit
from model.fda.fda_label_attr_page import FdaLabelAttrPage
from model.fda_scrape_versions import FdaScrapeVersions
from tools.fda.search_fdalabel_tradename.search_attr import (
    search_fdalabel_tradename_attr,
)


def search_fdalabel_tradename_indication_usages(
    tradename: str,
    *,
    versions: FdaScrapeVersions | None = None,
    maxn: int = 30,
    offset: int = 0,
    limit: int = 5,
) -> FdaLabelAttrPage[FdaLabelAttrHit]:
    """Search by tradename; return id/setid/tradename/indication_usages page."""
    return search_fdalabel_tradename_attr(
        FdaAttrName.INDICATION_USAGES,
        tradename,
        versions=versions,
        maxn=maxn,
        offset=offset,
        limit=limit,
    )
