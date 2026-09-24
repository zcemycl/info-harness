"""Map FdaAttrName → setid attr search callables."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from model.fda.fda_attr_name import FdaAttrName
from tools.fda.search_fdalabel_id import (
    adverse_effect_tables,
    adverse_effects,
    clinical_pharmacologies,
    clinical_trial_tables,
    clinical_trials,
    companies,
    contraindications,
    dosage_administrations,
    dosage_forms,
    drug_interactions,
    indication,
    indication_usages,
    supply_store_handles,
    therapeutic_areas,
    warning_precautions,
)

IdSearch = Callable[..., Any]

ID_ATTR_SEARCH: dict[FdaAttrName, IdSearch] = {
    FdaAttrName.INDICATION: indication.search_fdalabel_id_indication,
    FdaAttrName.INDICATION_USAGES: (
        indication_usages.search_fdalabel_id_indication_usages
    ),
    FdaAttrName.DOSAGE_ADMINISTRATIONS: (
        dosage_administrations.search_fdalabel_id_dosage_administrations
    ),
    FdaAttrName.DOSAGE_FORMS: dosage_forms.search_fdalabel_id_dosage_forms,
    FdaAttrName.CONTRAINDICATIONS: (
        contraindications.search_fdalabel_id_contraindications
    ),
    FdaAttrName.WARNING_PRECAUTIONS: (
        warning_precautions.search_fdalabel_id_warning_precautions
    ),
    FdaAttrName.ADVERSE_EFFECTS: adverse_effects.search_fdalabel_id_adverse_effects,
    FdaAttrName.ADVERSE_EFFECT_TABLES: (
        adverse_effect_tables.search_fdalabel_id_adverse_effect_tables
    ),
    FdaAttrName.DRUG_INTERACTIONS: (
        drug_interactions.search_fdalabel_id_drug_interactions
    ),
    FdaAttrName.CLINICAL_PHARMACOLOGIES: (
        clinical_pharmacologies.search_fdalabel_id_clinical_pharmacologies
    ),
    FdaAttrName.CLINICAL_TRIALS: clinical_trials.search_fdalabel_id_clinical_trials,
    FdaAttrName.CLINICAL_TRIAL_TABLES: (
        clinical_trial_tables.search_fdalabel_id_clinical_trial_tables
    ),
    FdaAttrName.SUPPLY_STORE_HANDLES: (
        supply_store_handles.search_fdalabel_id_supply_store_handles
    ),
    FdaAttrName.THERAPEUTIC_AREAS: (
        therapeutic_areas.search_fdalabel_id_therapeutic_areas
    ),
    FdaAttrName.COMPANIES: companies.search_fdalabel_id_companies,
}
