"""CLI subgroup: FDA label search by tradename (attr tools)."""

import typer

from cli.http.fda.search_tradename.register_attr_commands import (
    register_tradename_attr_commands,
)

app = typer.Typer(
    name="search-tradename",
    help="Search FDA labels by tradename (slim attr pages).",
    add_completion=False,
    no_args_is_help=True,
)

register_tradename_attr_commands(app)
