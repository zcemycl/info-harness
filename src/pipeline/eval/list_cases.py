"""List eval case ids under examples/eval/{layer}/."""

from __future__ import annotations

from model.eval.eval_layer import EvalLayer
from pipeline.eval.cases_root import eval_cases_root


def list_eval_case_ids(layer: EvalLayer) -> list[str]:
    """Return sorted case ids (JSON stems) for a layer."""
    folder = eval_cases_root() / layer.value
    if not folder.is_dir():
        return []
    return sorted(p.stem for p in folder.glob("*.json") if p.is_file())
