"""Load a single eval case JSON by layer and id."""

from __future__ import annotations

from model.eval.eval_layer import EvalLayer
from model.eval.inner_eval_case import InnerEvalCase
from model.eval.worker_eval_case import WorkerEvalCase
from pipeline.eval.cases_root import eval_cases_root


def load_eval_case(layer: EvalLayer, case_id: str) -> WorkerEvalCase | InnerEvalCase:
    """Load ``examples/eval/{layer}/{case_id}.json``."""
    path = eval_cases_root() / layer.value / f"{case_id}.json"
    if not path.is_file():
        raise FileNotFoundError(f"Eval case not found: {path}")
    raw = path.read_text(encoding="utf-8")
    if layer is EvalLayer.WORKER:
        return WorkerEvalCase.model_validate_json(raw)
    return InnerEvalCase.model_validate_json(raw)
