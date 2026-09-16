"""Thin CLI for FDA section scrape versions."""

from __future__ import annotations

import typer

from cli.http.dump_json import dump_json
from model.fda_scrape_versions import DEFAULT_SCRAPE_VERSION
from tools.fda.get_fdalabel_section_scrape_versions import (
    get_fdalabel_section_scrape_versions,
)


def section_scrape_versions(
    version: str = typer.Argument(
        DEFAULT_SCRAPE_VERSION, help="Parent FDA scrape version"
    ),
) -> None:
    """List section scrape versions for a parent version (HC API)."""
    try:
        results = get_fdalabel_section_scrape_versions(version)
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(dump_json(results))
