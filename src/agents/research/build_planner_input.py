"""Build the research planner user-message JSON payload."""

from __future__ import annotations

import json
from typing import Any

from model.research.diary_entry import DiaryEntry
from model.research.research_eval_result import ResearchEvalResult
from model.research.research_memory import ResearchMemory
from model.research.specialist_kind import SpecialistKind
from tools.research.collect_nct_ids_from_memory import collect_nct_ids_from_memory


def build_planner_input(
    brief: str,
    *,
    loop: int,
    diary: list[DiaryEntry],
    memory: ResearchMemory,
    eval_feedback: ResearchEvalResult | None,
) -> str:
    """Build planner user message with durable memory (not just last eval)."""
    payload: dict[str, Any] = {
        "brief": brief,
        "loop": loop,
        "available_specialists": [k.value for k in SpecialistKind],
        "known_ncts": collect_nct_ids_from_memory(memory),
        "latest_diary": diary[-1].model_dump(mode="json") if diary else None,
        "diary_tail": [e.model_dump(mode="json") for e in diary[-5:]],
        "memory": memory.model_dump(mode="json"),
        "memory_rules": {
            "do_not_repeat_settled_workstream_ids": list(memory.settled_ids()),
            "do_not_repeat_tried_ok_fingerprints": [
                t.fingerprint for t in memory.tried_ideas if t.status == "ok"
            ],
            "avoid_failed_approaches": memory.failed_approaches[-10:],
            "avoid_rejected_directions": memory.rejected_directions,
            "open_gaps": memory.open_gaps,
            "lessons": memory.lessons,
            "ctg_must_list_known_ncts_in_focus_and_seeds": True,
        },
    }
    if eval_feedback is not None:
        payload["evaluator_feedback"] = eval_feedback.model_dump(mode="json")
    return json.dumps(payload, indent=2, default=str)
