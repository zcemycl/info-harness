"""Typer sub-app for HC platform HTTP request tools."""

import typer

from cli.http.search_indication import search_indication
from cli.http.search_tradename import search_tradename

app = typer.Typer(
    name="http",
    help="Call HC platform HTTP endpoints.",
    add_completion=False,
    no_args_is_help=True,
)

app.command("search-indication")(search_indication)
app.command("search-tradename")(search_tradename)
