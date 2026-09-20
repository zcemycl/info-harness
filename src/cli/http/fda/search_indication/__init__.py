"""CLI subgroup: FDA label search by indication (attr tools)."""

import typer

from cli.http.fda.search_indication.register_attr_commands import (
    register_indication_attr_commands,
)

app = typer.Typer(
    name="search-indication",
    help="Search FDA labels by indication (slim attr pages).",
    add_completion=False,
    no_args_is_help=True,
)

register_indication_attr_commands(app)
