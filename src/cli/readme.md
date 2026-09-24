# CLI

Typer commands registered from `src/main.py`. Run from the repository root (Python 3.12+, [`uv`](https://docs.astral.sh/uv/)).

## How to run

```bash
uv run python src/main.py --help
uv run python src/main.py cognito-login -u USERNAME -p PASSWORD
uv run python src/main.py http --help
uv run python src/main.py http fda --help
uv run python src/main.py http fda search-tradename indication Keytruda
uv run python src/main.py http fda search-tradename adverse-effects Keytruda
uv run python src/main.py http ctg search-condition melanoma
uv run python src/main.py http ctg resolve-trial "INO-VATE"
uv run python src/main.py http ctg search-nctid basic-info NCT01234567
uv run python src/main.py http ctg search-nctid outcomes NCT01234567
uv run python src/main.py http ctg fetch-nctid basic-info NCT01234567
uv run python src/main.py http ctg fetch-nctid references NCT01234567
uv run python src/main.py http ta search immuno
uv run python src/main.py http pubmed search "pembrolizumab"
uv run python src/main.py http pubmed id-sections abstract 25712454
uv run python src/main.py agent ctg-search-nctid "outcomes for NCT01234567"
uv run python src/main.py agent ctg-fetch "latest status and PubMed refs for NCT01234567"
uv run python src/main.py agent pubmed-id-sections "abstract for PMID 25712454"
uv run python src/main.py agent pubmed-specialist "literature outcomes for PMID 25712454"
uv run python src/main.py agent ctg-search-condition "melanoma condition names"
uv run python src/main.py agent ctg-resolve-trial "resolve INO-VATE to an NCT"
uv run python src/main.py agent ctg-specialist "outcomes for NCT01234567"
```

## Notes

- All user-facing workflows go through `src/main.py`.
- One Typer command per file under `src/cli/`.
- HTTP CLIs live under `src/cli/http/<domain>/` and are mounted as `main.py http <domain> <command>`.
- Attr-scoped FDA searches are grouped as `http fda search-tradename|search-indication|search-id <attr>`.
- Attr-scoped CTG **HC** searches: `http ctg search-nctid <attr>` (`basic-info`, `demographics`, `conditions`, `locations`, `adverse-events`, `outcomes`).
- Attr-scoped CTG **live** fetch: `http ctg fetch-nctid <attr>` (same sections plus `references` for PMIDs / see-also links).
- Attr-scoped PubMed **PMID** fetch: `http pubmed id-sections <attr>` (`citation`, `abstract`, `authors`, `mesh`, `chemicals`, `publication-types`, `keywords`, `secondary-ids`).
- CTG resolve: `http ctg resolve-trial` maps study names / protocol ids → NCT via CT.gov + PubMed.
- CTG agents: `ctg-search-nctid` (HC), `ctg-fetch` (live CT.gov), `ctg-search-condition`, `ctg-resolve-trial`, `ctg-specialist`.
- PubMed agents: `pubmed-id-sections` (PMID sections), `pubmed-specialist`.
- Command bodies stay thin — call into `tools/` (preferred) or `hc_http/`.
