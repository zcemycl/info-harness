"""Register one Typer command per CTG study section for live NCT-id fetch."""

from __future__ import annotations

from collections.abc import Callable

import typer

from cli.http.dump_json import dump_json
from model.ctg.ctg_attr_name import CtgAttrName
from tools.ctg.fetch_ctg_nctid.attr_registry import NCTID_ATTR_FETCH


def register_fetch_nctid_attr_commands(app: typer.Typer) -> None:
    """Attach ``basic-info``, ``demographics``, … commands to ``app``."""
    for attr, fetch in NCTID_ATTR_FETCH.items():
        app.command(attr.value.replace("_", "-"))(_make_command(attr, fetch))


def _make_command(attr: CtgAttrName, fetch: object) -> Callable[..., None]:
    def command(
        nctid: str = typer.Argument(..., help="NCT id to fetch, e.g. NCT01234567"),
        offset: int = typer.Option(0, "--offset", help="Result offset"),
        limit: int = typer.Option(5, "--limit", help="Result limit"),
    ) -> None:
        try:
            results = fetch(  # type: ignore[operator]
                nctid,
                offset=offset,
                limit=limit,
            )
        except (FileNotFoundError, RuntimeError, ValueError) as exc:
            typer.secho(str(exc), fg=typer.colors.RED, err=True)
            raise typer.Exit(code=1) from exc
        typer.echo(dump_json(results))

    command.__name__ = attr.value
    command.__doc__ = f"Fetch live CT.gov by NCT id; return {attr.value} page."
    return command
