# info-harness

CLI and agent harness for ingest / tool / workflow experiments.

Layout and conventions mirror a thin Typer + `uv` project: sole entry at `src/main.py`, one command per file under `src/cli/`, HTTP clients in `src/hc_http/` (domain folders), pipelines in `src/pipeline/`, models in `src/model/`, prompts in `src/prompt/`, agents in `src/agents/`, tools in `src/tools/` (domain folders).

## Prerequisites

- Python 3.12 or later
- [`uv`](https://docs.astral.sh/uv/getting-started/installation/) for environment and dependency management

## Setup

```bash
# Install deps including lint tools (creates .venv, writes uv.lock)
uv sync --group dev

# Install git hooks (black, isort, flake8, mypy)
uv run pre-commit install

# Optional: copy env template and edit locally (never commit .env)
cp .env.example .env
```

## Basic commands

```bash
# CLI help
uv run python src/main.py --help

# Cognito login (saves JWTs to `.cognito_tokens.json`)
uv run python src/main.py cognito-login -u USERNAME -p PASSWORD

# HC HTTP subgroups (mirrors hc-backend routers)
uv run python src/main.py http --help
uv run python src/main.py http fda search-tradename indication Keytruda
uv run python src/main.py http fda search-indication indication melanoma
uv run python src/main.py http fda search-by-compare-filters --filters-json '{"filters":null}'
uv run python src/main.py http ctg search-condition melanoma
uv run python src/main.py http ctg search-nctid basic-info NCT01234567
uv run python src/main.py http ctg search-nctid outcomes NCT01234567
uv run python src/main.py http ctg search-by-compare-filters --filters-json '{"filters":null}'
uv run python src/main.py http ta search immuno
uv run python src/main.py http ta search immuno --both-sides   # %q% vs default q%
uv run python src/main.py http pubmed search "pembrolizumab melanoma"

# Agents (FDA / ICD / CTG workers + specialists)
uv run python src/main.py agent --help
uv run python src/main.py agent icd-ta-worker "find TA names for immuno"
uv run python src/main.py agent icd-ta-specialist "What ICD therapeutic areas match oncology?"
uv run python src/main.py agent fda-label-specialist "What are the FDA-approved indications for Keytruda?"
uv run python src/main.py agent ctg-search-nctid "outcomes and demographics for NCT01234567"
uv run python src/main.py agent ctg-search-condition "CTG condition names for melanoma"
uv run python src/main.py agent ctg-specialist "What are the outcomes for NCT01234567?"

# Eval (FDA workers + inner specialist; fixtures + optional LLM judge)
uv run python src/main.py eval --help
uv run python src/main.py eval run --layer worker
uv run python src/main.py eval run --layer inner
uv run python src/main.py eval run --layer all
uv run python src/main.py eval run --layer inner --case hiv_drugs_by_tradename
uv run python src/main.py eval run --layer all --no-judge   # fixtures only
```

Cases live under `src/examples/eval/{worker,inner}/`; reports under `data/eval/{suite_id}/`. Pass requires fixtures and (unless `--no-judge`) an LLM score ≥ `FDA_EVAL_PASS_THRESHOLD` (default `3.5`).

CI runs the same lint suite via [`.github/workflows/lint.yml`](.github/workflows/lint.yml).
See [`src/cli/readme.md`](src/cli/readme.md) for CLI conventions.

## Layout

```text
src/
  main.py          # sole CLI entry (registers commands only)
  cli/
    http/          # main.py http <domain> <command>
      fda/
      ctg/
      therapeutic_area/
      pubmed/
  hc_http/         # HTTP clients by domain (HC + PubMed E-utils)
    fda/
    ctg/
    therapeutic_area/
    pubmed/
  pipeline/        # ingest / preprocess / run steps
  model/           # pydantic schemas (fda/, ctg/, pubmed/ + request models)
  prompt/          # prompts only
  agents/          # one folder per agent
  tools/           # agent-facing wrappers by domain
    fda/
    ctg/
    therapeutic_area/
    pubmed/
  examples/        # few-shot examples
tests/
data/              # local inputs (gitignored artefacts as needed)
```

Cursor rules under `.cursor/rules/` enforce CLI entry, layout, and module style (200-line cap, one primary unit per file).
