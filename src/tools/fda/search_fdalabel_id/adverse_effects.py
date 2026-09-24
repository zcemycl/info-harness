"""Search FDA labels by setid; return adverse_effects hits only."""

from __future__ import annotations

from model.fda.fda_attr_name import FdaAttrName
from model.fda.fda_label_attr_hit import FdaLabelAttrHit
from model.fda.fda_label_attr_page import FdaLabelAttrPage
from model.fda_scrape_versions import FdaScrapeVersions
from tools.fda.search_fdalabel_id.search_attr import search_fdalabel_id_attr


def search_fdalabel_id_adverse_effects(
    setid: str,
    *,
    versions: FdaScrapeVersions | None = None,
    maxn: int = 30,
    offset: int = 0,
    limit: int = 5,
) -> FdaLabelAttrPage[FdaLabelAttrHit]:
    """Search by setid; return id/setid/tradename/adverse_effects page."""
    return search_fdalabel_id_attr(
        FdaAttrName.ADVERSE_EFFECTS,
        setid,
        versions=versions,
        maxn=maxn,
        offset=offset,
        limit=limit,
    )
