"""Project one FdaLabel field into an FdaLabelAttrHit."""

from __future__ import annotations

from typing import Any

from model.fda.fda_attr_name import FdaAttrName
from model.fda.fda_label import FdaLabel
from model.fda.fda_label_attr_hit import FdaLabelAttrHit
from model.fda.fda_label_section import FdaLabelSection


def project_attr_hit(label: FdaLabel, attr: FdaAttrName) -> FdaLabelAttrHit:
    """Keep id/setid/tradename plus one attr; strip section embeddings."""
    return FdaLabelAttrHit(
        id=label.id,
        setid=label.setid,
        tradename=label.tradename,
        attr=attr,
        value=_strip_value(getattr(label, attr.value)),
    )


def _strip_value(value: Any) -> Any:
    if isinstance(value, list):
        return [_strip_item(item) for item in value]
    return value


def _strip_item(item: Any) -> Any:
    if isinstance(item, FdaLabelSection):
        return item.model_copy(update={"embedding": None})
    if hasattr(item, "model_dump"):
        return item
    return item
