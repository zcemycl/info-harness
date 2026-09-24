"""FDA label response model mirroring hc-backend FdaLabel."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from model.fda.company import CompanyBase
from model.fda.fda_label_section import FdaLabelSection
from model.fda.fda_label_table import FdaLabelTable
from model.fda.therapeutic_area import TherapeuticArea


class FdaLabel(BaseModel):
    """Full FDA label document returned by HC search endpoints."""

    model_config = ConfigDict(extra="allow")

    id: int = Field(description="Internal FDA label row id")
    tradename: str = Field(description="Drug trade name")
    setid: UUID = Field(description="SPL setid UUID")
    pdf_link: str = Field(description="Link to label PDF")
    xml_link: str = Field(description="Link to label XML")
    distance: float | None = Field(
        default=None,
        description="Similarity/distance score on indication or TA search",
    )
    manufacturer: str | None = Field(
        default=None, description="Manufacturer display name"
    )
    initial_us_approval_year: int | None = Field(
        default=None, description="Initial US approval year when known"
    )
    spl_earliest_date: datetime | None = Field(
        default=None, description="Earliest SPL date"
    )
    spl_effective_date: datetime | None = Field(
        default=None, description="Effective SPL date"
    )
    version: str | None = Field(
        default=None, description="FDA label scrape version pin"
    )
    indication: str | None = Field(
        default=None, description="Primary indication text summary"
    )
    indication_usages: list[FdaLabelSection] | None = Field(
        default=None, description="Section 1 indication/usage blocks"
    )
    dosage_administrations: list[FdaLabelSection] | None = Field(
        default=None, description="Section 2 dosage & administration"
    )
    dosage_forms: list[FdaLabelSection] | None = Field(
        default=None, description="Section 3 dosage forms"
    )
    contraindications: list[FdaLabelSection] | None = Field(
        default=None, description="Section 4 contraindications"
    )
    warning_precautions: list[FdaLabelSection] | None = Field(
        default=None, description="Section 5 warnings/precautions"
    )
    adverse_effects: list[FdaLabelSection] | None = Field(
        default=None, description="Section 6 adverse effects text"
    )
    adverse_effect_tables: list[FdaLabelTable] | None = Field(
        default=None, description="Parsed adverse-effect tables"
    )
    drug_interactions: list[FdaLabelSection] | None = Field(
        default=None, description="Section 7 drug interactions"
    )
    clinical_pharmacologies: list[FdaLabelSection] | None = Field(
        default=None, description="Section 12 clinical pharmacology"
    )
    clinical_trials: list[FdaLabelSection] | None = Field(
        default=None, description="Section 14 clinical trial text"
    )
    clinical_trial_tables: list[FdaLabelTable] | None = Field(
        default=None, description="Parsed clinical-trial tables"
    )
    supply_store_handles: list[FdaLabelSection] | None = Field(
        default=None, description="Section 16 how supplied/storage"
    )
    therapeutic_areas: list[TherapeuticArea] | None = Field(
        default=None, description="Linked therapeutic area nodes"
    )
    companies: list[CompanyBase] | None = Field(
        default=None, description="Linked company records"
    )
    ae_tables_count: int = Field(description="Count of AE tables on the label")
    ct_tables_count: int = Field(description="Count of CT tables on the label")
