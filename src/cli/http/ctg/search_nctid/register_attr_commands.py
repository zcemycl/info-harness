"""Register one Typer command per CTG study section for NCT-id search."""

from __future__ import annotations

from collections.abc import Callable

import typer

from cli.http.dump_json import dump_json
from hc_http.ctg.get_by_nctids import DEFAULT_CACHE_KEY
from model.ctg.ctg_attr_name import CtgAttrName
from model.fda_scrape_versions import DEFAULT_SCRAPE_VERSION
from tools.ctg.search_ctg_nctid.attr_registry import NCTID_ATTR_SEARCH


def register_nctid_attr_commands(app: typer.Typer) -> None:
    """Attach ``basic-info``, ``demographics``, … commands to ``app``."""
    for attr, search in NCTID_ATTR_SEARCH.items():
        app.command(attr.value.replace("_", "-"))(_make_command(attr, search))


def _make_command(attr: CtgAttrName, search: object) -> Callable[..., None]:
    def command(
        nctid: str = typer.Argument(..., help="NCT id to search, e.g. NCT01234567"),
        version: str = typer.Option(
            DEFAULT_SCRAPE_VERSION,
            "--version",
            "-v",
            help="CTG row version",
        ),
        cache_key: str = typer.Option(
            DEFAULT_CACHE_KEY, "--cache-key", help="Server-side cache key"
        ),
        offset: int = typer.Option(0, "--offset", help="Result offset"),
        limit: int = typer.Option(5, "--limit", help="Result limit"),
    ) -> None:
        try:
            results = search(  # type: ignore[operator]
                nctid,
                version=version,
                cache_key=cache_key,
                offset=offset,
                limit=limit,
            )
        except (FileNotFoundError, RuntimeError, ValueError) as exc:
            typer.secho(str(exc), fg=typer.colors.RED, err=True)
            raise typer.Exit(code=1) from exc
        typer.echo(dump_json(results))

    command.__name__ = attr.value
    command.__doc__ = f"Search by NCT id; return {attr.value} page."
    return command
