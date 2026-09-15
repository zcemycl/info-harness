"""Thin CLI for FDA compare-filter count."""

from __future__ import annotations

import json

import typer

from cli.http.parse_json_object import parse_json_object
from hc_http.fda.count_by_compare_filters import DEFAULT_CACHE_KEY
from model.advanced_filters import AdvancedFilterPayload
from model.fda_scrape_versions import DEFAULT_SCRAPE_VERSION, FdaScrapeVersions
from tools.fda.count_fdalabel_by_compare_filters import (
    count_fdalabel_by_compare_filters,
)


def count_by_compare_filters(
    filters_json: str = typer.Option(
        '{"filters": null}',
        "--filters-json",
        help="AdvancedFilterPayload JSON",
    ),
    version: str = typer.Option(
        DEFAULT_SCRAPE_VERSION, "--version", "-v", help="Scrape version"
    ),
    embedding_threshold: float = typer.Option(0.6, "--embedding-threshold"),
    cache_key: str = typer.Option(DEFAULT_CACHE_KEY, "--cache-key"),
) -> None:
    """Count FDA labels matching compare filters (HC API)."""
    try:
        result = count_fdalabel_by_compare_filters(
            advanced_filter=AdvancedFilterPayload.model_validate(
                parse_json_object(filters_json, label="--filters-json")
            ),
            versions=FdaScrapeVersions.all(version),
            embedding_threshold=embedding_threshold,
            cache_key=cache_key,
        )
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(json.dumps(result, indent=2))
