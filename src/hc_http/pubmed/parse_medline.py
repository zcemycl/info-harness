"""Parse NCBI MEDLINE plain-text into MedlineRecord rows."""

from __future__ import annotations

from model.pubmed.medline_record import MedlineRecord

_TAG_WIDTH = 4


def parse_medline(text: str) -> list[MedlineRecord]:
    """Split efetch medline text into records; join continuation lines."""
    records: list[MedlineRecord] = []
    current: dict[str, list[str]] = {}
    last_tag: str | None = None

    def _flush() -> None:
        nonlocal current, last_tag
        if not current:
            return
        pmids = current.get("PMID") or []
        pmid = (pmids[0] if pmids else "").strip()
        if pmid:
            records.append(MedlineRecord(pmid=pmid, tags=dict(current)))
        current = {}
        last_tag = None

    for raw_line in text.splitlines():
        line = raw_line.rstrip("\n")
        if not line.strip():
            _flush()
            continue
        if (
            len(line) > _TAG_WIDTH
            and line[_TAG_WIDTH] == "-"
            and line[:_TAG_WIDTH].strip()
        ):
            tag = line[:_TAG_WIDTH].strip()
            value = line[_TAG_WIDTH + 1 :].strip()
            current.setdefault(tag, []).append(value)
            last_tag = tag
            continue
        if line.startswith("      ") and last_tag is not None:
            cont = line.strip()
            values = current.setdefault(last_tag, [])
            if values:
                values[-1] = f"{values[-1]} {cont}".strip()
            else:
                values.append(cont)
            continue
    _flush()
    return records
