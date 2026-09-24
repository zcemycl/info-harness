"""Thin CLI for FDA compare-filter search."""

from __future__ import annotations

import typer

from cli.http.dump_json import dump_json
from cli.http.parse_json_object import parse_json_object
from hc_http.fda.search_by_compare_filters import DEFAULT_CACHE_KEY
from model.advanced_filters import AdvancedFilterPayload
from model.fda_scrape_versions import DEFAULT_SCRAPE_VERSION, FdaScrapeVersions
from model.refine_filters import RefineFilters
from tools.fda.search_fdalabel_by_compare_filters import (
    search_fdalabel_by_compare_filters,
)


def search_by_compare_filters(
    filters_json: str = typer.Option(
        '{"filters": null}',
        "--filters-json",
        help="AdvancedFilterPayload JSON",
    ),
    refined_json: str = typer.Option("{}", "--refined-json", help="RefineFilters JSON"),
    version: str = typer.Option(
        DEFAULT_SCRAPE_VERSION, "--version", "-v", help="Scrape version"
    ),
    limit: int = typer.Option(10, "--limit"),
    offset: int = typer.Option(0, "--offset"),
    embedding_threshold: float = typer.Option(0.6, "--embedding-threshold"),
    cache_key: str = typer.Option(DEFAULT_CACHE_KEY, "--cache-key"),
) -> None:
    """Search FDA labels by compare filters (HC API)."""
    try:
        results = search_fdalabel_by_compare_filters(
            advanced_filter=AdvancedFilterPayload.model_validate(
                parse_json_object(filters_json, label="--filters-json")
            ),
            refined_filters=RefineFilters.model_validate(
                parse_json_object(refined_json, label="--refined-json")
            ),
            versions=FdaScrapeVersions.all(version),
            limit=limit,
            offset=offset,
            embedding_threshold=embedding_threshold,
            cache_key=cache_key,
        )
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(dump_json(results))
