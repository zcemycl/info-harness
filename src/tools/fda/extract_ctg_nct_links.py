"""Extract canonical NCT ids and CTG study URLs from free text."""

from __future__ import annotations

import re

from model.fda.ctg_nct_link import CtgNctLink

_NCT_RE = re.compile(r"\bNCT[-\s]?(\d{8})\b", re.IGNORECASE)
_CTG_STUDY_URL = "https://clinicaltrials.gov/study/{nctid}"


def extract_ctg_nct_links(text: str) -> list[CtgNctLink]:
    """Pull unique NCT######## ids from text (e.g. clinical_trials content)."""
    if not text:
        return []
    seen: set[str] = set()
    links: list[CtgNctLink] = []
    for match in _NCT_RE.finditer(text):
        nctid = f"NCT{match.group(1)}"
        if nctid in seen:
            continue
        seen.add(nctid)
        links.append(
            CtgNctLink(nctid=nctid, ctg_url=_CTG_STUDY_URL.format(nctid=nctid))
        )
    return links
