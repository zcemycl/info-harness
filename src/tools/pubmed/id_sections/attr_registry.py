"""Map PubmedAttrName → PMID id-section callables."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from model.pubmed.pubmed_attr_name import PubmedAttrName
from tools.pubmed.id_sections import (
    abstract,
    authors,
    chemicals,
    citation,
    keywords,
    mesh,
    publication_types,
    secondary_ids,
)

PmidFetch = Callable[..., Any]

ID_ATTR_SECTIONS: dict[PubmedAttrName, PmidFetch] = {
    PubmedAttrName.CITATION: citation.pubmed_id_citation,
    PubmedAttrName.ABSTRACT: abstract.pubmed_id_abstract,
    PubmedAttrName.AUTHORS: authors.pubmed_id_authors,
    PubmedAttrName.MESH: mesh.pubmed_id_mesh,
    PubmedAttrName.CHEMICALS: chemicals.pubmed_id_chemicals,
    PubmedAttrName.PUBLICATION_TYPES: publication_types.pubmed_id_publication_types,
    PubmedAttrName.KEYWORDS: keywords.pubmed_id_keywords,
    PubmedAttrName.SECONDARY_IDS: secondary_ids.pubmed_id_secondary_ids,
}
