"""CLI subgroup: live CT.gov fetch by NCT id (section attr tools)."""

import typer

from cli.http.ctg.fetch_nctid.register_attr_commands import (
    register_fetch_nctid_attr_commands,
)

app = typer.Typer(
    name="fetch-nctid",
    help=(
        "Fetch live ClinicalTrials.gov by NCT id "
        "(same sections as search-nctid, plus references)."
    ),
    add_completion=False,
    no_args_is_help=True,
)

register_fetch_nctid_attr_commands(app)
