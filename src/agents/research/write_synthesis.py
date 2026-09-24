"""Writer step: synthesize a cross-specialist answer."""

from __future__ import annotations

import json

from agents.chat_model import chat_model
from model.research.research_pack import ResearchPack
from model.research.research_plan import ResearchPlan
from prompt.load_prompt import load_prompt
from tools.research.prefer_ctg_or_fda import prefer_ctg_or_fda


def write_synthesis(
    brief: str,
    plan: ResearchPlan,
    pack: ResearchPack,
) -> str:
    """Ask the writer LLM for a plain-text synthesized answer."""
    llm = chat_model(model_env="OPENROUTER_RESEARCH_WRITER_MODEL")
    payload = {
        "brief": brief,
        "plan": plan.model_dump(mode="json"),
        "nct_source_priority": prefer_ctg_or_fda(pack),
        "outcomes": [
            {
                "workstream_id": o.workstream_id,
                "specialist": o.specialist.value,
                "focus": o.brief.focus,
                "status": o.status.value,
                "answer": o.answer.answer,
                "error": o.error,
            }
            for o in pack.outcomes
        ],
    }
    response = llm.invoke(
        [
            {"role": "system", "content": load_prompt("research", "writer.md")},
            {
                "role": "user",
                "content": json.dumps(payload, indent=2, default=str),
            },
        ]
    )
    content = response.content
    return content if isinstance(content, str) else str(content)
