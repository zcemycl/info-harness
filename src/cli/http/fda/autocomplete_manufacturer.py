"""Thin CLI wrapper for FDA manufacturer autocomplete."""

from __future__ import annotations

import json

import typer

from hc_http.fda._cache_key import DEFAULT_CACHE_KEY
from model.fda_scrape_versions import DEFAULT_SCRAPE_VERSION, FdaScrapeVersions
from tools.fda.autocomplete_fdalabel_manufacturer import (
    autocomplete_fdalabel_manufacturer,
)


def autocomplete_manufacturer(
    manufacturer: str = typer.Argument(..., help="Manufacturer prefix/query"),
    version: str = typer.Option(
        DEFAULT_SCRAPE_VERSION,
        "--version",
        "-v",
        help="Scrape version applied to every cache/version field",
    ),
    cache_key: str = typer.Option(
        DEFAULT_CACHE_KEY, "--cache-key", help="Server-side cache key"
    ),
) -> None:
    """Autocomplete FDA manufacturers (HC API)."""
    try:
        results = autocomplete_fdalabel_manufacturer(
            manufacturer,
            versions=FdaScrapeVersions.all(version),
            cache_key=cache_key,
        )
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(json.dumps(results, indent=2))
