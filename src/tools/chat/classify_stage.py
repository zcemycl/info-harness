"""Label a diary stage as an outer loop, inner loop, or worker."""

from __future__ import annotations

from typing import Literal

from model.research.agent_answer import AgentAnswer

_INNER = frozenset({"fda", "ctg", "pubmed", "icd"})
_PEWE = frozenset({"planner", "executor", "writer", "evaluator"})
Tier = Literal["outer", "inner", "worker"]


def classify_stage(entry: AgentAnswer) -> tuple[Tier, str, str | None]:
    """Return ``(tier, domain, stage)`` for a streamed stage event."""
    layer, stage = _path_parts(entry.path)
    agent = (entry.agent or "step").strip() or "step"
    if stage not in _PEWE:
        stage = agent if agent in _PEWE else None
    domain = layer or agent
    if domain == "research" or agent == "research":
        return "outer", "research", stage if domain == "research" else None
    if domain in _INNER:
        return "inner", domain, stage
    return "worker", domain, None


def _path_parts(path: str | None) -> tuple[str | None, str | None]:
    if not path:
        return None, None
    parts = [part for part in path.split("/") if part]
    try:
        rest = parts[parts.index("diary") + 2 :]
    except ValueError:
        rest = parts
    body = rest[:-1] if rest and rest[-1].endswith(".json") else rest
    if not body:
        return None, None
    stage = body[2] if len(body) >= 3 and body[1].startswith("loop-") else None
    return body[0], stage
