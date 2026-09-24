"""CLI subgroup: PubMed fetch by PMID (section attr tools)."""

import typer

from cli.http.pubmed.id_sections.register_attr_commands import (
    register_id_section_commands,
)

app = typer.Typer(
    name="id-sections",
    help="Fetch PubMed MEDLINE by PMID (slim section pages).",
    add_completion=False,
    no_args_is_help=True,
)

register_id_section_commands(app)
