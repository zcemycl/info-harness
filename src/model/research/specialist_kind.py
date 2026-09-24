"""Domain specialist kinds the research outer loop may spawn."""

from __future__ import annotations

from enum import StrEnum


class SpecialistKind(StrEnum):
    """Callable specialist pipelines (PubMed deferred)."""

    FDA_LABEL = "fda_label"
    CTG = "ctg"
    ICD_TA = "icd_ta"
