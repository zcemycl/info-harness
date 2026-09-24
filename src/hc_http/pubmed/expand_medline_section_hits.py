"""Expand a projected MEDLINE section into one PubmedAttrHit per unit."""

from __future__ import annotations

from typing import Any

from model.pubmed.pubmed_attr_hit import PubmedAttrHit
from model.pubmed.pubmed_attr_name import PubmedAttrName

_ABSTRACT_CHUNK = 800


def expand_medline_section_hits(
    pmid: str,
    attr: PubmedAttrName,
    value: Any,
) -> list[PubmedAttrHit]:
    """Split section payloads so each hit is small enough for full evidence notes."""
    units = _units(attr, value)
    if not units:
        return [PubmedAttrHit(pmid=pmid, attr=attr, value=None)]
    return [PubmedAttrHit(pmid=pmid, attr=attr, value=unit) for unit in units]


def _units(attr: PubmedAttrName, value: Any) -> list[Any]:
    if value is None:
        return []
    if attr is PubmedAttrName.CITATION and isinstance(value, dict):
        return [value]
    if attr is PubmedAttrName.ABSTRACT and isinstance(value, str):
        return _chunk_text(value)
    if attr is PubmedAttrName.AUTHORS and isinstance(value, list):
        return list(value)
    if attr in (
        PubmedAttrName.MESH,
        PubmedAttrName.CHEMICALS,
        PubmedAttrName.PUBLICATION_TYPES,
        PubmedAttrName.KEYWORDS,
    ) and isinstance(value, list):
        return list(value)
    if attr is PubmedAttrName.SECONDARY_IDS and isinstance(value, list):
        return list(value)
    return [value]


def _chunk_text(text: str) -> list[str]:
    cleaned = " ".join(text.split())
    if not cleaned:
        return []
    if len(cleaned) <= _ABSTRACT_CHUNK:
        return [cleaned]
    chunks: list[str] = []
    start = 0
    while start < len(cleaned):
        end = min(start + _ABSTRACT_CHUNK, len(cleaned))
        if end < len(cleaned):
            space = cleaned.rfind(" ", start, end)
            if space > start:
                end = space
        piece = cleaned[start:end].strip()
        if piece:
            chunks.append(piece)
        start = end if end > start else end + 1
    return chunks
