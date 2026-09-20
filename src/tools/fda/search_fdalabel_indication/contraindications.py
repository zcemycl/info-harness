"""Search FDA labels by indication; return contraindications hits only."""

from __future__ import annotations

from hc_http.fda._cache_key import DEFAULT_CACHE_KEY
from hc_http.fda.search_by_indication import DEFAULT_SORT_BY
from model.fda.fda_attr_name import FdaAttrName
from model.fda.fda_label_attr_hit import FdaLabelAttrHit
from model.fda.fda_label_attr_page import FdaLabelAttrPage
from model.fda_scrape_versions import FdaScrapeVersions
from tools.fda.search_fdalabel_indication.search_attr import (
    search_fdalabel_indication_attr,
)


def search_fdalabel_indication_contraindications(
    indication: str,
    *,
    versions: FdaScrapeVersions | None = None,
    maxn: int = 30,
    offset: int = 0,
    limit: int = 5,
    sort_by: str = DEFAULT_SORT_BY,
    cache_key: str = DEFAULT_CACHE_KEY,
) -> FdaLabelAttrPage[FdaLabelAttrHit]:
    """Search by indication; return id/setid/tradename/contraindications page."""
    return search_fdalabel_indication_attr(
        FdaAttrName.CONTRAINDICATIONS,
        indication,
        versions=versions,
        maxn=maxn,
        offset=offset,
        limit=limit,
        sort_by=sort_by,
        cache_key=cache_key,
    )
