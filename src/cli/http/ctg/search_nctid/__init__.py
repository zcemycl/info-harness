"""CLI subgroup: CTG search by NCT id (section attr tools)."""

import typer

from cli.http.ctg.search_nctid.register_attr_commands import (
    register_nctid_attr_commands,
)

app = typer.Typer(
    name="search-nctid",
    help="Search CTG studies by NCT id (slim section pages).",
    add_completion=False,
    no_args_is_help=True,
)

register_nctid_attr_commands(app)
