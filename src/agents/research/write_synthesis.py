"""Writer step: synthesize a cross-specialist answer."""

from __future__ import annotations

import json

from agents.chat_model import chat_model
from agents.research.invoke_text_with_reader import invoke_text_with_reader
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
                "workstream_id": item.workstream_id,
                "specialist": item.specialist.value,
                "focus": item.brief.focus,
                "status": item.status.value,
                "answer_path": item.answer.path,
                "total_chars": len(item.answer.answer or ""),
                "error": item.error,
            }
            for item in pack.outcomes
        ],
    }
    return invoke_text_with_reader(
        llm,
        system=load_prompt("research", "writer.md"),
        user=json.dumps(payload, indent=2, default=str),
    )
