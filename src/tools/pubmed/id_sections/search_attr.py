"""Fetch PubMed by PMID and project one fixed MEDLINE section."""

from __future__ import annotations

from hc_http.pubmed.project_pubmed_id_hits import project_pubmed_id_hits
from model.pubmed.pubmed_attr_hit import PubmedAttrHit
from model.pubmed.pubmed_attr_name import PubmedAttrName
from model.pubmed.pubmed_attr_page import PubmedAttrPage
from tools.trace_call import trace_info, trace_span
from tools.wrap_attr_page import wrap_attr_page


def pubmed_id_attr(
    attr: PubmedAttrName,
    pmid: str,
    *,
    offset: int = 0,
    limit: int = 20,
) -> PubmedAttrPage[PubmedAttrHit]:
    """Fetch by PMID; return expanded pmid/<attr> page."""
    with trace_span(
        "tool",
        f"pubmed_id_{attr.value}",
        pmid=pmid,
        offset=offset,
        limit=limit,
    ):
        projected = project_pubmed_id_hits(pmid, attr)
        page_items = projected[offset : offset + limit]
        page = wrap_attr_page(page_items, offset=offset, limit=limit)
        trace_info(
            "page",
            items=len(page.items),
            total=len(projected),
            next_offset=page.next_offset,
        )
        return page
