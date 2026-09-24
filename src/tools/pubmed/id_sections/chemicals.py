"""Fetch PubMed by PMID; return chemicals section only."""

from __future__ import annotations

from model.pubmed.pubmed_attr_hit import PubmedAttrHit
from model.pubmed.pubmed_attr_name import PubmedAttrName
from model.pubmed.pubmed_attr_page import PubmedAttrPage
from tools.pubmed.id_sections.search_attr import pubmed_id_attr


def pubmed_id_chemicals(
    pmid: str,
    *,
    offset: int = 0,
    limit: int = 20,
) -> PubmedAttrPage[PubmedAttrHit]:
    """Fetch by PMID; return chemicals page."""
    return pubmed_id_attr(PubmedAttrName.CHEMICALS, pmid, offset=offset, limit=limit)
