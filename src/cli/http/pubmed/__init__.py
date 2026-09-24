"""CLI subgroup for PubMed / NCBI E-utilities."""

import typer

from cli.http.pubmed.fetch_summaries import fetch_summaries
from cli.http.pubmed.id_sections import app as id_sections_app
from cli.http.pubmed.search import search

app = typer.Typer(
    name="pubmed",
    help="PubMed NCBI E-utilities (not HC platform).",
    add_completion=False,
    no_args_is_help=True,
)

app.command("search")(search)
app.command("fetch-summaries")(fetch_summaries)
app.add_typer(id_sections_app, name="id-sections")
