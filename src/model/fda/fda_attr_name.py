"""Fixed FDA label attribute names for attr-scoped tools (not free-form)."""

from __future__ import annotations

from enum import StrEnum


class FdaAttrName(StrEnum):
    """Every FdaLabel section/field exposed as its own tool."""

    INDICATION = "indication"
    INDICATION_USAGES = "indication_usages"
    DOSAGE_ADMINISTRATIONS = "dosage_administrations"
    DOSAGE_FORMS = "dosage_forms"
    CONTRAINDICATIONS = "contraindications"
    WARNING_PRECAUTIONS = "warning_precautions"
    ADVERSE_EFFECTS = "adverse_effects"
    ADVERSE_EFFECT_TABLES = "adverse_effect_tables"
    DRUG_INTERACTIONS = "drug_interactions"
    CLINICAL_PHARMACOLOGIES = "clinical_pharmacologies"
    CLINICAL_TRIALS = "clinical_trials"
    CLINICAL_TRIAL_TABLES = "clinical_trial_tables"
    SUPPLY_STORE_HANDLES = "supply_store_handles"
    THERAPEUTIC_AREAS = "therapeutic_areas"
    COMPANIES = "companies"
