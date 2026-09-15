"""Thin CLI wrapper for FDA label search by exact manufacturer."""

from __future__ import annotations

import json

import typer

from model.fda_scrape_versions import DEFAULT_SCRAPE_VERSION, FdaScrapeVersions
from tools.fda.search_fdalabel_by_manufacturer import search_fdalabel_by_manufacturer


def search_by_manufacturer(
    manufacturer: str = typer.Argument(..., help="Exact manufacturer name"),
    version: str = typer.Option(
        DEFAULT_SCRAPE_VERSION,
        "--version",
        "-v",
        help="Scrape version applied to every cache/version field",
    ),
) -> None:
    """Search FDA labels by exact manufacturer (HC API)."""
    try:
        results = search_fdalabel_by_manufacturer(
            manufacturer, versions=FdaScrapeVersions.all(version)
        )
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(json.dumps(results, indent=2))
