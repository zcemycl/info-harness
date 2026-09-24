"""Fetch MEDLINE by PMID and project one PubmedAttrName into hits."""

from __future__ import annotations

from hc_http.pubmed.expand_medline_section_hits import expand_medline_section_hits
from hc_http.pubmed.fetch_medline import run_fetch_medline
from hc_http.pubmed.parse_medline import parse_medline
from hc_http.pubmed.project_medline_section import project_medline_section
from model.pubmed.pubmed_attr_hit import PubmedAttrHit
from model.pubmed.pubmed_attr_name import PubmedAttrName


def project_pubmed_id_hits(pmid: str, attr: PubmedAttrName) -> list[PubmedAttrHit]:
    """efetch one PMID, parse, project attr, expand to pageable hits."""
    nid = pmid.strip()
    if not nid.isdigit():
        raise ValueError(f"invalid PMID: {pmid!r}")
    text = run_fetch_medline([nid])
    records = parse_medline(text)
    if not records:
        raise RuntimeError(f"No MEDLINE record for PMID {nid}")
    record = next((r for r in records if r.pmid == nid), records[0])
    value = project_medline_section(record, attr)
    return expand_medline_section_hits(record.pmid, attr, value)
