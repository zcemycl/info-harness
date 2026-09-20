"""Final answer synthesis for the ICD therapeutic-area specialist."""

from __future__ import annotations

import json

from agents.chat_model import chat_model
from model.therapeutic_area.icd_evidence_note import IcdEvidenceNote


def synthesize_icd_answer(brief: str, evidence: list[IcdEvidenceNote]) -> str:
    """Write a short answer from the brief and collected TA name evidence."""
    llm = chat_model(model_env="OPENROUTER_FDA_SPECIALIST_MODEL")
    payload = {
        "brief": brief,
        "evidence": [n.model_dump(mode="json") for n in evidence],
    }
    response = llm.invoke(
        [
            {
                "role": "system",
                "content": (
                    "Answer the brief using only the evidence notes. "
                    "List concrete therapeutic area names from evidence. "
                    "Do not invent names. Be concise."
                ),
            },
            {
                "role": "user",
                "content": json.dumps(payload, indent=2, default=str),
            },
        ]
    )
    content = response.content
    return content if isinstance(content, str) else str(content)
