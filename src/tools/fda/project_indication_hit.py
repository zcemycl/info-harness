"""Project a full FdaLabel into an indication-only hit."""

from __future__ import annotations

from model.fda.fda_label import FdaLabel
from model.fda.fda_label_indication_hit import FdaLabelIndicationHit


def project_indication_hit(label: FdaLabel) -> FdaLabelIndicationHit:
    """Keep id/setid/tradename/indication only."""
    return FdaLabelIndicationHit(
        id=label.id,
        setid=label.setid,
        tradename=label.tradename,
        indication=label.indication,
    )
