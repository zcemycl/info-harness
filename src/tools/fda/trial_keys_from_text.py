"""Extract trial/protocol keys from FDA table captions or prose."""

from __future__ import annotations

from tools.fda.extract_ctg_nct_links import extract_ctg_nct_links
from tools.fda.extract_study_mentions import extract_study_mentions


def trial_keys_from_text(text: str) -> list[str]:
    """Return unique NCT / protocol / acronym keys found in ``text``."""
    if not text:
        return []
    keys: list[str] = []
    seen: set[str] = set()
    for link in extract_ctg_nct_links(text):
        key = link.nctid.upper()
        if key not in seen:
            seen.add(key)
            keys.append(key)
    for mention in extract_study_mentions(text):
        key = mention.raw.strip()
        if not key:
            continue
        norm = key.casefold()
        if norm in seen:
            continue
        seen.add(norm)
        keys.append(key)
    return keys
