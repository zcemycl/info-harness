"""Collect unique real PubMed PMIDs from free text."""

from __future__ import annotations

import re

from model.pubmed.is_placeholder_pmid import is_placeholder_pmid

_LABELED = re.compile(r"(?i)\bPMID[:\s#]*(\d{5,9})\b")
_KNOWN_LIST = re.compile(r"(?i)Known PMID(?:s)?[:\s]+((?:\d{5,9}(?:\s*,\s*|\s+))+)")
_BARE = re.compile(r"^\d{5,9}$")


def collect_pmids(*texts: str | None) -> list[str]:
    """Return unique non-placeholder PMIDs found across the given strings."""
    seen: set[str] = set()
    out: list[str] = []
    for text in texts:
        if not text:
            continue
        for match in _LABELED.finditer(text):
            _add(match.group(1), seen, out)
        for match in _KNOWN_LIST.finditer(text):
            for pmid in re.findall(r"\d{5,9}", match.group(1)):
                _add(pmid, seen, out)
        stripped = text.strip()
        if _BARE.fullmatch(stripped):
            _add(stripped, seen, out)
        elif len(stripped) <= 200 and re.search(r"\d{5,9}", stripped):
            # seed-like lists: "28171899, 27269947" without PMID label
            if "," in stripped or stripped.lower().startswith("known"):
                for part in re.split(r"[\s,;]+", stripped):
                    if _BARE.fullmatch(part):
                        _add(part, seen, out)
    return out


def _add(pmid: str, seen: set[str], out: list[str]) -> None:
    if pmid in seen or is_placeholder_pmid(pmid):
        return
    seen.add(pmid)
    out.append(pmid)
