# Commands

Run from the repository root (Python 3.12+, [`uv`](https://docs.astral.sh/uv/)).

```bash
# CLI help
uv run python src/main.py --help

# Cognito login (saves JWTs to `.cognito_tokens.json`)
uv run python src/main.py cognito-login -u USERNAME -p PASSWORD
```

## HC HTTP

Mirrors hc-backend routers under `http <domain> <command>`.

```bash
uv run python src/main.py http --help

# FDA
uv run python src/main.py http fda search-tradename indication Keytruda
uv run python src/main.py http fda search-indication indication melanoma
uv run python src/main.py http fda search-by-compare-filters --filters-json '{"filters":null}'

# ClinicalTrials.gov (HC + live CT.gov)
uv run python src/main.py http ctg search-condition melanoma
uv run python src/main.py http ctg resolve-trial "INO-VATE"
uv run python src/main.py http ctg search-nctid basic-info NCT01234567
uv run python src/main.py http ctg search-nctid outcomes NCT01234567
uv run python src/main.py http ctg fetch-nctid basic-info NCT01234567   # live CT.gov
uv run python src/main.py http ctg fetch-nctid references NCT01234567  # PMIDs / see-also
uv run python src/main.py http ctg search-by-compare-filters --filters-json '{"filters":null}'

# Therapeutic area
uv run python src/main.py http ta search immuno
uv run python src/main.py http ta search immuno --both-sides   # %q% vs default q%

# PubMed
uv run python src/main.py http pubmed search "pembrolizumab melanoma"
uv run python src/main.py http pubmed id-sections abstract 25712454
uv run python src/main.py http pubmed id-sections citation 25712454
```

Notes:

- Attr-scoped FDA: `http fda search-tradename|search-indication|search-id <attr>`
- Attr-scoped CTG HC: `http ctg search-nctid <attr>` (`basic-info`, `demographics`, `conditions`, `locations`, `adverse-events`, `outcomes`)
- Attr-scoped CTG live: `http ctg fetch-nctid <attr>` (same sections plus `references`)
- Attr-scoped PubMed PMID: `http pubmed id-sections <attr>` (`citation`, `abstract`, `authors`, `mesh`, `chemicals`, `publication-types`, `keywords`, `secondary-ids`)

## Agents

Workers, specialists (inner PEWE), and the research outer loop.

```bash
uv run python src/main.py agent --help

# Workers
uv run python src/main.py agent icd-ta-worker "find TA names for immuno"
uv run python src/main.py agent ctg-search-nctid "outcomes and demographics for NCT01234567"
uv run python src/main.py agent ctg-fetch "latest status and PubMed refs for NCT01234567"
uv run python src/main.py agent ctg-search-condition "CTG condition names for melanoma"
uv run python src/main.py agent ctg-resolve-trial "resolve INO-VATE to an NCT id"
uv run python src/main.py agent pubmed-id-sections "abstract and citation for PMID 25712454"

# Specialists (inner PEWE)
uv run python src/main.py agent icd-ta-specialist "What ICD therapeutic areas match oncology?"
uv run python src/main.py agent fda-label-specialist "What are the FDA-approved indications for Keytruda?"
uv run python src/main.py agent ctg-specialist "What are the outcomes for NCT01234567?"
uv run python src/main.py agent pubmed-specialist "literature outcomes for PMID 25712454"

# Research (outer PEWE)
uv run python src/main.py agent research "Keytruda indications and related pivotal trials"
```

## Eval

Fixtures under `src/examples/eval/{worker,inner}/`; reports under `data/eval/{suite_id}/`.

```bash
uv run python src/main.py eval --help
uv run python src/main.py eval run --layer worker
uv run python src/main.py eval run --layer worker --case nct01564784_outcomes
uv run python src/main.py eval run --layer worker --case nct01564784_setup_conditions_outcomes
uv run python src/main.py eval run --layer inner
uv run python src/main.py eval run --layer all
uv run python src/main.py eval run --layer inner --case hiv_drugs_by_tradename
uv run python src/main.py eval run --layer worker --case besponsa_clinical_trials_nct
uv run python src/main.py eval run --layer inner --case besponsa_clinical_trials_nct
uv run python src/main.py eval run --layer all --no-judge   # fixtures only
```

Pass requires fixtures and (unless `--no-judge`) an LLM score ≥ `FDA_EVAL_PASS_THRESHOLD` (default `3.5`).

See [`src/cli/readme.md`](../src/cli/readme.md) for CLI conventions.
