"""Detect whether a user brief is asking for literature / PubMed."""

from __future__ import annotations

import re

_LIT = re.compile(
    r"(?i)\b("
    r"pubmed|pmid|pmids|literature|publication|publications|"
    r"paper|papers|article|articles|journal|medline|citation|citations"
    r")\b"
)


def brief_wants_literature(*texts: str | None) -> bool:
    """True when any text clearly asks for PubMed / published literature."""
    for text in texts:
        if text and _LIT.search(text):
            return True
    return False
