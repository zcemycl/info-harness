"""Typer sub-app for HC platform HTTP request tools."""

import typer

from cli.http.ctg import app as ctg_app
from cli.http.fda import app as fda_app
from cli.http.pubmed import app as pubmed_app
from cli.http.therapeutic_area import app as ta_app

app = typer.Typer(
    name="http",
    help="Call HC platform (and PubMed) HTTP endpoints.",
    add_completion=False,
    no_args_is_help=True,
)

app.add_typer(fda_app, name="fda")
app.add_typer(ctg_app, name="ctg")
app.add_typer(ta_app, name="ta")
app.add_typer(pubmed_app, name="pubmed")
