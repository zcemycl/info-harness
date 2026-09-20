"""Register one Typer command per FdaLabel attr for indication search."""

from __future__ import annotations

from collections.abc import Callable

import typer

from cli.http.dump_json import dump_json
from hc_http.fda._cache_key import DEFAULT_CACHE_KEY
from hc_http.fda.search_by_indication import DEFAULT_SORT_BY
from model.fda.fda_attr_name import FdaAttrName
from model.fda_scrape_versions import DEFAULT_SCRAPE_VERSION, FdaScrapeVersions
from tools.fda.search_fdalabel_indication.attr_registry import INDICATION_ATTR_SEARCH


def register_indication_attr_commands(app: typer.Typer) -> None:
    """Attach ``indication``, ``adverse-effects``, … commands to ``app``."""
    for attr, search in INDICATION_ATTR_SEARCH.items():
        app.command(attr.value.replace("_", "-"))(_make_command(attr, search))


def _make_command(attr: FdaAttrName, search: object) -> Callable[..., None]:
    def command(
        indication_query: str = typer.Argument(
            ..., metavar="INDICATION", help="Indication text to search"
        ),
        version: str = typer.Option(
            DEFAULT_SCRAPE_VERSION,
            "--version",
            "-v",
            help="Scrape version applied to every cache/version field",
        ),
        maxn: int = typer.Option(30, "--maxn", help="Max candidates"),
        offset: int = typer.Option(0, "--offset", help="Result offset"),
        limit: int = typer.Option(5, "--limit", help="Result limit"),
        sort_by: str = typer.Option(
            DEFAULT_SORT_BY, "--sort-by", help="Sort order (e.g. relevance)"
        ),
        cache_key: str = typer.Option(
            DEFAULT_CACHE_KEY, "--cache-key", help="Server-side cache key"
        ),
    ) -> None:
        try:
            results = search(  # type: ignore[operator]
                indication_query,
                versions=FdaScrapeVersions.all(version),
                maxn=maxn,
                offset=offset,
                limit=limit,
                sort_by=sort_by,
                cache_key=cache_key,
            )
        except (FileNotFoundError, RuntimeError, ValueError) as exc:
            typer.secho(str(exc), fg=typer.colors.RED, err=True)
            raise typer.Exit(code=1) from exc
        typer.echo(dump_json(results))

    command.__name__ = attr.value
    command.__doc__ = f"Search by indication; return {attr.value} page."
    return command
