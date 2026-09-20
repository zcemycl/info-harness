"""Register one Typer command per FdaLabel attr for setid search."""

from __future__ import annotations

from collections.abc import Callable

import typer

from cli.http.dump_json import dump_json
from model.fda.fda_attr_name import FdaAttrName
from model.fda_scrape_versions import DEFAULT_SCRAPE_VERSION, FdaScrapeVersions
from tools.fda.search_fdalabel_id.attr_registry import ID_ATTR_SEARCH


def register_id_attr_commands(app: typer.Typer) -> None:
    """Attach ``indication``, ``adverse-effects``, … commands to ``app``."""
    for attr, search in ID_ATTR_SEARCH.items():
        app.command(attr.value.replace("_", "-"))(_make_command(attr, search))


def _make_command(attr: FdaAttrName, search: object) -> Callable[..., None]:
    def command(
        setid: str = typer.Argument(..., help="FDA label setid to search"),
        version: str = typer.Option(
            DEFAULT_SCRAPE_VERSION,
            "--version",
            "-v",
            help="Scrape version applied to every cache/version field",
        ),
        maxn: int = typer.Option(30, "--maxn", help="Max candidates"),
        offset: int = typer.Option(0, "--offset", help="Result offset"),
        limit: int = typer.Option(5, "--limit", help="Result limit"),
    ) -> None:
        try:
            results = search(  # type: ignore[operator]
                setid,
                versions=FdaScrapeVersions.all(version),
                maxn=maxn,
                offset=offset,
                limit=limit,
            )
        except (FileNotFoundError, RuntimeError, ValueError) as exc:
            typer.secho(str(exc), fg=typer.colors.RED, err=True)
            raise typer.Exit(code=1) from exc
        typer.echo(dump_json(results))

    command.__name__ = attr.value
    command.__doc__ = f"Search by setid; return {attr.value} page."
    return command
