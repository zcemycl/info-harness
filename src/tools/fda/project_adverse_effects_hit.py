"""Project a full FdaLabel into an adverse-effects-only hit."""

from __future__ import annotations

from model.fda.fda_label import FdaLabel
from model.fda.fda_label_adverse_effects_hit import FdaLabelAdverseEffectsHit
from model.fda.fda_label_section import FdaLabelSection


def project_adverse_effects_hit(label: FdaLabel) -> FdaLabelAdverseEffectsHit:
    """Keep id/setid/tradename/adverse_effects; drop embeddings."""
    sections = label.adverse_effects
    if sections is not None:
        sections = [_without_embedding(s) for s in sections]
    return FdaLabelAdverseEffectsHit(
        id=label.id,
        setid=label.setid,
        tradename=label.tradename,
        adverse_effects=sections,
    )


def _without_embedding(section: FdaLabelSection) -> FdaLabelSection:
    return section.model_copy(update={"embedding": None})
