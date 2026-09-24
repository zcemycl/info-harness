"""Project one PubmedAttrName section from a MedlineRecord."""

from __future__ import annotations

from typing import Any

from model.pubmed.medline_record import MedlineRecord
from model.pubmed.pubmed_attr_name import PubmedAttrName


def project_medline_section(record: MedlineRecord, attr: PubmedAttrName) -> Any:
    """Return the raw section value for one attr (pre-expand)."""
    tags = record.tags
    if attr is PubmedAttrName.CITATION:
        title = _first(tags, "TI") or _first(tags, "BTI")
        journal = _first(tags, "JT") or _first(tags, "TA") or _first(tags, "CTI")
        source = _first(tags, "SO") or _book_source(tags)
        return {
            "title": title,
            "journal": journal,
            "date": _first(tags, "DP"),
            "volume": _first(tags, "VI"),
            "issue": _first(tags, "IP"),
            "pages": _first(tags, "PG"),
            "source": source,
            "publisher": _first(tags, "PB"),
            "place": _first(tags, "PL"),
        }
    if attr is PubmedAttrName.ABSTRACT:
        return _first(tags, "AB")
    if attr is PubmedAttrName.AUTHORS:
        return _authors(tags)
    if attr is PubmedAttrName.MESH:
        return list(tags.get("MH") or [])
    if attr is PubmedAttrName.CHEMICALS:
        return list(tags.get("RN") or []) + list(tags.get("NM") or [])
    if attr is PubmedAttrName.PUBLICATION_TYPES:
        return list(tags.get("PT") or [])
    if attr is PubmedAttrName.KEYWORDS:
        return list(tags.get("OT") or [])
    if attr is PubmedAttrName.SECONDARY_IDS:
        return _secondary_ids(tags)
    raise ValueError(f"Unsupported PubMed attr: {attr}")


def _first(tags: dict[str, list[str]], key: str) -> str | None:
    values = tags.get(key) or []
    return values[0] if values else None


def _book_source(tags: dict[str, list[str]]) -> str | None:
    """Build a SO-like line for book/report records (BTI/CTI/PB)."""
    bits = [
        part
        for part in (
            _first(tags, "PB"),
            _first(tags, "PL"),
            _first(tags, "DP"),
            _first(tags, "CTI"),
        )
        if part
    ]
    return ". ".join(bits) if bits else None


def _authors(tags: dict[str, list[str]]) -> list[dict[str, str | None]]:
    aus = list(tags.get("AU") or [])
    faus = list(tags.get("FAU") or [])
    ads = list(tags.get("AD") or [])
    n = max(len(aus), len(faus), 1 if ads else 0)
    out: list[dict[str, str | None]] = []
    for i in range(max(n, len(aus), len(faus))):
        out.append(
            {
                "au": aus[i] if i < len(aus) else None,
                "fau": faus[i] if i < len(faus) else None,
                "ad": ads[i] if i < len(ads) else None,
            }
        )
    return [row for row in out if row["au"] or row["fau"]]


def _secondary_ids(tags: dict[str, list[str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for aid in tags.get("AID") or []:
        rows.append({"kind": "aid", "value": aid})
    for lid in tags.get("LID") or []:
        rows.append({"kind": "lid", "value": lid})
    for pmc in tags.get("PMC") or []:
        rows.append({"kind": "pmc", "value": pmc})
    for si in tags.get("SI") or []:
        rows.append({"kind": "si", "value": si})
    return rows
