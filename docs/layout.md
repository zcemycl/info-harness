# Project layout

Thin Typer + `uv` project. Sole entry at `src/main.py`; one command per file under `src/cli/`. Cursor rules under `.cursor/rules/` enforce CLI entry, layout, and module style (200-line cap, one primary unit per file).

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
  agents/          # one folder per agent (workers, specialists, research)
  tools/           # agent-facing wrappers by domain
    fda/
    ctg/
    therapeutic_area/
    pubmed/
    chat/          # chat history, briefs, run events
  api/             # FastAPI (local uvicorn + Lambda Mangum)
  examples/        # few-shot examples + eval fixtures
tests/
web/               # static chatbot for GitHub Pages
data/              # local inputs (gitignored artefacts as needed)
docs/
  commands.md
  layout.md
```

## Conventions

| Folder | Purpose |
|--------|---------|
| `src/cli/` | Typer handlers — one command per file |
| `src/hc_http/` | HTTP clients by domain |
| `src/pipeline/` | Ingestion, preprocessing, orchestration |
| `src/model/` | Pydantic schemas only |
| `src/prompt/` | LLM prompt templates |
| `src/agents/` | Agents SDK agents — one agent per subfolder |
| `src/tools/` | Callable tools wrapping `hc_http/` |
| `src/api/` | FastAPI app; Lambda handler `api.lambda_handler.handler`. CLI stays `src/main.py` |
| `web/` | Static chatbot |
| `src/examples/` | Few-shot examples and eval cases |

Do **not** name a top-level package `http` — it shadows the Python stdlib.
