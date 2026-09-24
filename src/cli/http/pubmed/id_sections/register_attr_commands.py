"""Register one Typer command per PubMed MEDLINE section for PMID fetch."""

from __future__ import annotations

from collections.abc import Callable

import typer

from cli.http.dump_json import dump_json
from model.pubmed.pubmed_attr_name import PubmedAttrName
from tools.pubmed.id_sections.attr_registry import ID_ATTR_SECTIONS


def register_id_section_commands(app: typer.Typer) -> None:
    """Attach ``citation``, ``abstract``, … commands to ``app``."""
    for attr, fetch in ID_ATTR_SECTIONS.items():
        app.command(attr.value.replace("_", "-"))(_make_command(attr, fetch))


def _make_command(attr: PubmedAttrName, fetch: object) -> Callable[..., None]:
    def command(
        pmid: str = typer.Argument(..., help="PubMed PMID, e.g. 25712454"),
        offset: int = typer.Option(0, "--offset", help="Result offset"),
        limit: int = typer.Option(20, "--limit", help="Result limit"),
    ) -> None:
        try:
            results = fetch(  # type: ignore[operator]
                pmid,
                offset=offset,
                limit=limit,
            )
        except (FileNotFoundError, RuntimeError, ValueError) as exc:
            typer.secho(str(exc), fg=typer.colors.RED, err=True)
            raise typer.Exit(code=1) from exc
        typer.echo(dump_json(results))

    command.__name__ = attr.value
    command.__doc__ = f"Fetch PubMed by PMID; return {attr.value} page."
    return command
