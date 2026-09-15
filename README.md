# info-harness

CLI and agent harness for ingest / tool / workflow experiments.

Layout and conventions mirror a thin Typer + `uv` project: sole entry at `src/main.py`, one command per file under `src/cli/`, HTTP clients in `src/hc_http/`, pipelines in `src/pipeline/`, models in `src/model/`, prompts in `src/prompt/`, agents in `src/agents/`, tools in `src/tools/`.

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

# HC HTTP subgroup
uv run python src/main.py http --help
uv run python src/main.py http search-tradename Keytruda
uv run python src/main.py http search-indication melanoma
```

CI runs the same lint suite via [`.github/workflows/lint.yml`](.github/workflows/lint.yml).
See [`src/cli/readme.md`](src/cli/readme.md) for CLI conventions.

## Layout

```text
src/
  main.py          # sole CLI entry (registers commands only)
  cli/             # one Typer command per file
    http/          # main.py http <command>
  hc_http/         # HC platform HTTP clients / requests
  pipeline/        # ingest / preprocess / run steps
  model/           # pydantic only
  prompt/          # prompts only
  agents/          # one folder per agent
  tools/           # callable tools (auth helpers, etc.)
  examples/        # few-shot examples
tests/
data/              # local inputs (gitignored artefacts as needed)
```

Cursor rules under `.cursor/rules/` enforce CLI entry, layout, and module style (200-line cap, one primary unit per file).
