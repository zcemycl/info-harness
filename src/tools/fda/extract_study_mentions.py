"""Extract non-NCT study mentions (protocol ids / acronyms) from label text."""

from __future__ import annotations

import re

from model.fda.study_mention import StudyMention, StudyMentionKind
from tools.ctg.expand_trial_aliases import expand_trial_aliases

# Sponsor-style protocol ids common in FDA Section 14 (GSK CNA*, Pfizer B*, …)
_PROTOCOL_RE = re.compile(
    r"\b("
    r"CNAA?\d{3,6}"
    r"|B\d{6,8}"
    r"|ESS\d{5,8}"
    r"|ING\d{5,8}"
    r"|GSK\d{5,10}"
    r")\b",
    re.IGNORECASE,
)
# Hyphenated or spaced acronyms like INO-VATE / INO VATE (2–4 letter chunks)
_ACRONYM_RE = re.compile(r"\b([A-Z]{2,6}(?:[-\s][A-Z]{2,6}){1,3})\b")
_NCT_RE = re.compile(r"\bNCT[-\s]?\d{8}\b", re.IGNORECASE)


def extract_study_mentions(text: str) -> list[StudyMention]:
    """Pull unique non-NCT protocol ids and acronym-like study names."""
    if not text:
        return []
    # Drop NCT spans so we don't treat them as protocol tokens
    cleaned = _NCT_RE.sub(" ", text)
    seen: set[str] = set()
    mentions: list[StudyMention] = []

    for match in _PROTOCOL_RE.finditer(cleaned):
        raw = match.group(1)
        key = raw.casefold()
        if key in seen:
            continue
        seen.add(key)
        aliases = [a for a in expand_trial_aliases(raw) if a.casefold() != key]
        mentions.append(
            StudyMention(
                raw=raw,
                kind=StudyMentionKind.PROTOCOL_ID,
                aliases=aliases,
            )
        )

    for match in _ACRONYM_RE.finditer(cleaned):
        raw = re.sub(r"\s+", "-", match.group(1).strip())
        key = raw.casefold()
        if key in seen:
            continue
        # Skip tokens that look like plain English all-caps words without hyphen
        if "-" not in raw and len(raw) > 6:
            continue
        seen.add(key)
        aliases = [a for a in expand_trial_aliases(raw) if a.casefold() != key]
        mentions.append(
            StudyMention(
                raw=raw,
                kind=StudyMentionKind.ACRONYM,
                aliases=aliases,
            )
        )
    return mentions
