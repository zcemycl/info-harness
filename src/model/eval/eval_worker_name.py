"""Worker names accepted by worker-layer eval cases (FDA + CTG)."""

from __future__ import annotations

from enum import StrEnum


class EvalWorkerName(StrEnum):
    """Axis worker the case should dispatch."""

    TRADENAME = "tradename"
    INDICATION = "indication"
    ID = "id"
    THERAPEUTIC_AREA = "therapeutic_area"
    NCTID = "nctid"
    CONDITION = "condition"
    RESOLVE_TRIAL = "resolve_trial"
