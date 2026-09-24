"""Final answer synthesis for the FDA label specialist."""

from __future__ import annotations

import json

from agents.chat_model import chat_model
from model.research.evidence_note import EvidenceNote
from tools.evidence.compact_evidence_notes import compact_evidence_notes


def synthesize_fda_answer(brief: str, evidence: list[EvidenceNote]) -> str:
    """Write a short answer from the brief and collected evidence notes."""
    llm = chat_model(model_env="OPENROUTER_FDA_SPECIALIST_MODEL")
    payload = {
        "brief": brief,
        "evidence": compact_evidence_notes(evidence, tail=None),
    }
    response = llm.invoke(
        [
            {
                "role": "system",
                "content": (
                    "Answer the brief using only the evidence notes. "
                    "Cite tradename and setid. Be concise. "
                    "When NCT ids or CTG links appear in evidence, copy them "
                    "exactly (clinicaltrials.gov/study/… URLs). "
                    "Do not invent NCT ids or /ct2/show/ links. "
                    "For each subindication/title section, cite ≥1 pivotal "
                    "trial (NCT or protocol id). For adverse effects, cite "
                    "both ae_reaction and laboratory tables when present "
                    "(use Table N / kind= from notes). Prefer linked table "
                    "grids over prose alone for numeric rates."
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
