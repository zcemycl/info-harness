"""Fixed PubMed MEDLINE section names for attr-scoped tools."""

from __future__ import annotations

from enum import StrEnum


class PubmedAttrName(StrEnum):
    """Every MEDLINE projection exposed as its own pubmed_id tool."""

    CITATION = "citation"
    ABSTRACT = "abstract"
    AUTHORS = "authors"
    MESH = "mesh"
    CHEMICALS = "chemicals"
    PUBLICATION_TYPES = "publication_types"
    KEYWORDS = "keywords"
    SECONDARY_IDS = "secondary_ids"
