"""FDA scrape section version pins for HC API requests."""

from pydantic import BaseModel, Field

DEFAULT_SCRAPE_VERSION = "v0.0.4"


class FdaScrapeVersions(BaseModel):
    """Version map sent as the FDA/CTG search request body."""

    fdalabel: str | None = Field(
        default=DEFAULT_SCRAPE_VERSION,
        description="Parent FDA label scrape version",
    )
    indication_usage: str | None = Field(
        default=DEFAULT_SCRAPE_VERSION, description="Section 1 version"
    )
    dosage_administration: str | None = Field(
        default=DEFAULT_SCRAPE_VERSION, description="Section 2 version"
    )
    dosage_form: str | None = Field(
        default=DEFAULT_SCRAPE_VERSION, description="Section 3 version"
    )
    contraindication: str | None = Field(
        default=DEFAULT_SCRAPE_VERSION, description="Section 4 version"
    )
    warning_precaution: str | None = Field(
        default=DEFAULT_SCRAPE_VERSION, description="Section 5 version"
    )
    adverse_effect: str | None = Field(
        default=DEFAULT_SCRAPE_VERSION, description="Section 6 text version"
    )
    adverse_effect_table: str | None = Field(
        default=DEFAULT_SCRAPE_VERSION, description="AE table version"
    )
    drug_interaction: str | None = Field(
        default=DEFAULT_SCRAPE_VERSION, description="Section 7 version"
    )
    clinical_pharmacology: str | None = Field(
        default=DEFAULT_SCRAPE_VERSION, description="Section 12 version"
    )
    clinical_trial: str | None = Field(
        default=DEFAULT_SCRAPE_VERSION, description="Section 14 text version"
    )
    clinical_trial_table: str | None = Field(
        default=DEFAULT_SCRAPE_VERSION, description="CT table version"
    )
    supply_store_handle: str | None = Field(
        default=DEFAULT_SCRAPE_VERSION, description="Section 16 version"
    )

    @classmethod
    def all(cls, version: str = DEFAULT_SCRAPE_VERSION) -> "FdaScrapeVersions":
        """Return a versions map with every field set to `version`."""
        fields = {name: version for name in cls.model_fields}
        return cls(**fields)
