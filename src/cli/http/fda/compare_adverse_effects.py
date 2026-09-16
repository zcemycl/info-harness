"""Thin CLI for FDA adverse-effects compare."""

from __future__ import annotations

import typer

from cli.http.dump_json import dump_json
from model.fda_scrape_versions import DEFAULT_SCRAPE_VERSION, FdaScrapeVersions
from tools.fda.compare_fdalabel_adverse_effects import (
    compare_fdalabel_adverse_effects,
)


def compare_adverse_effects(
    setid: list[str] = typer.Argument(..., help="One or more setids"),
    version: str = typer.Option(
        DEFAULT_SCRAPE_VERSION, "--version", "-v", help="Scrape version"
    ),
) -> None:
    """Compare adverse-effects tables across setids (HC API)."""
    try:
        results = compare_fdalabel_adverse_effects(
            setid, versions=FdaScrapeVersions.all(version)
        )
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(dump_json(results))
