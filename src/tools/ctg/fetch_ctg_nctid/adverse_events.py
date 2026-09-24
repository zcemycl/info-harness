"""Fetch live CT.gov by NCT id; return adverse_events section only."""

from __future__ import annotations

from model.ctg.ctg_attr_hit import CtgAttrHit
from model.ctg.ctg_attr_name import CtgAttrName
from model.ctg.ctg_attr_page import CtgAttrPage
from tools.ctg.fetch_ctg_nctid.search_attr import fetch_ctg_nctid_attr


def fetch_ctg_nctid_adverse_events(
    nctid: str,
    *,
    offset: int = 0,
    limit: int = 5,
) -> CtgAttrPage[CtgAttrHit]:
    """Fetch by NCT id; return adverse_events page."""
    return fetch_ctg_nctid_attr(
        CtgAttrName.ADVERSE_EVENTS, nctid, offset=offset, limit=limit
    )
