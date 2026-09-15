"""FDA scrape section version pins for HC API requests."""

from pydantic import BaseModel, Field

DEFAULT_SCRAPE_VERSION = "v0.0.4"


class FdaScrapeVersions(BaseModel):
    """Version map sent as the FDA label search request body."""

    fdalabel: str | None = Field(default=DEFAULT_SCRAPE_VERSION)
    indication_usage: str | None = Field(default=DEFAULT_SCRAPE_VERSION)
    dosage_administration: str | None = Field(default=DEFAULT_SCRAPE_VERSION)
    dosage_form: str | None = Field(default=DEFAULT_SCRAPE_VERSION)
    contraindication: str | None = Field(default=DEFAULT_SCRAPE_VERSION)
    warning_precaution: str | None = Field(default=DEFAULT_SCRAPE_VERSION)
    adverse_effect: str | None = Field(default=DEFAULT_SCRAPE_VERSION)
    adverse_effect_table: str | None = Field(default=DEFAULT_SCRAPE_VERSION)
    drug_interaction: str | None = Field(default=DEFAULT_SCRAPE_VERSION)
    clinical_pharmacology: str | None = Field(default=DEFAULT_SCRAPE_VERSION)
    clinical_trial: str | None = Field(default=DEFAULT_SCRAPE_VERSION)
    clinical_trial_table: str | None = Field(default=DEFAULT_SCRAPE_VERSION)
    supply_store_handle: str | None = Field(default=DEFAULT_SCRAPE_VERSION)

    @classmethod
    def all(cls, version: str = DEFAULT_SCRAPE_VERSION) -> "FdaScrapeVersions":
        """Return a versions map with every field set to `version`."""
        fields = {name: version for name in cls.model_fields}
        return cls(**fields)
