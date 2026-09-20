"""CLI subgroup: FDA label search by setid (attr tools)."""

import typer

from cli.http.fda.search_id.register_attr_commands import register_id_attr_commands

app = typer.Typer(
    name="search-id",
    help="Search FDA labels by setid (slim attr pages).",
    add_completion=False,
    no_args_is_help=True,
)

register_id_attr_commands(app)
