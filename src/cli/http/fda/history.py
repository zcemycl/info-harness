"""Thin CLI wrapper for FDA label history by setid."""

from __future__ import annotations

import json

import typer

from model.fda_scrape_versions import DEFAULT_SCRAPE_VERSION, FdaScrapeVersions
from tools.fda.fdalabel_history_by_id import fdalabel_history_by_id


def history(
    setid: str = typer.Argument(..., help="FDA label setid"),
    version: str = typer.Option(
        DEFAULT_SCRAPE_VERSION,
        "--version",
        "-v",
        help="Scrape version applied to every cache/version field",
    ),
) -> None:
    """Fetch FDA label history by setid (HC API)."""
    try:
        results = fdalabel_history_by_id(setid, versions=FdaScrapeVersions.all(version))
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(json.dumps(results, indent=2))
