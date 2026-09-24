"""Collect unique real NCT ids from free text."""

from __future__ import annotations

from tools.fda.extract_ctg_nct_links import extract_ctg_nct_links


def collect_nct_ids(*texts: str | None) -> list[str]:
    """Return unique NCT######## ids found across the given strings."""
    seen: set[str] = set()
    out: list[str] = []
    for text in texts:
        if not text:
            continue
        for link in extract_ctg_nct_links(text):
            if link.nctid not in seen:
                seen.add(link.nctid)
                out.append(link.nctid)
    return out
