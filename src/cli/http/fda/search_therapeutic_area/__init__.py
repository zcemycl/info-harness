"""CLI subgroup: FDA label search by therapeutic area (attr tools)."""

import typer

from cli.http.fda.search_therapeutic_area.register_attr_commands import (
    register_therapeutic_area_attr_commands,
)

app = typer.Typer(
    name="search-therapeutic-area",
    help="Search FDA labels by therapeutic area (slim attr pages).",
    add_completion=False,
    no_args_is_help=True,
)

register_therapeutic_area_attr_commands(app)
