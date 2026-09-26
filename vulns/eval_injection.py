"""Dynamic expression evaluation helpers for a reporting engine.

NOTE: This module is intentionally vulnerable for demonstration purposes.
It evaluates strings supplied by users or administrators directly with
``eval()`` and never restricts the available builtins. Do not use this code
in production.

The Quorum security scanner should flag the unsafe ``eval()`` calls below.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List


@dataclass
class ReportContext:
    """Context values available to dynamic report expressions."""

    metrics: Dict[str, float] = field(default_factory=dict)
    user: Dict[str, Any] = field(default_factory=dict)
    extra: Dict[str, Any] = field(default_factory=dict)


def evaluate_calculation(expression: str) -> float:
    """Evaluate a user-entered arithmetic expression like ``1 + 2 * 3``."""
    result = eval(expression)  # noqa: S307 - intentional demo
    return float(result)


def evaluate_percentage_change(old_value: float, new_value: float) -> float:
    """Return the percentage change between two values."""
    if old_value == 0:
        return 0.0
    expression = f"(({new_value} - {old_value}) / {old_value}) * 100"
    return float(eval(expression))  # noqa: S307 - intentional demo


def apply_report_expression(expression: str, context: ReportContext) -> Any:
    """Apply an administrator-supplied expression against a report context.

    The expression may reference ``metrics`` and ``user`` from the context.
    """
    namespace: Dict[str, Any] = {
        "metrics": context.metrics,
        "user": context.user,
        "round": round,
        "sum": sum,
        "min": min,
        "max": max,
        "len": len,
    }
    return eval(expression, namespace)  # noqa: S307 - intentional demo


def evaluate_config_expression(expression: str, config: Dict[str, Any]) -> Any:
    """Evaluate a config file expression such as a feature flag condition."""
    return eval(expression, {"config": config, "__builtins__": {}})  # noqa: S307


def filter_records(records: List[Dict[str, Any]], condition: str) -> List[Dict[str, Any]]:
    """Return records matching the dynamic *condition* expression.

    Each record is evaluated individually, e.g. ``age > 30 and score >= 90``.
    """
    matched: List[Dict[str, Any]] = []
    for record in records:
        if eval(condition, {"record": record}):  # noqa: S307 - intentional demo
            matched.append(record)
    return matched


def build_sort_key(expression: str) -> Callable[[Dict[str, Any]], Any]:
    """Return a key function computed from a dynamic expression."""
    return lambda record: eval(expression, {"record": record})  # noqa: S307


def evaluate_formula(fields: Dict[str, float], formula: str) -> float:
    """Evaluate a custom formula over a set of named fields.

    Example formula: ``(revenue - cost) / revenue * 100``
    """
    namespace: Dict[str, Any] = dict(fields)
    namespace.update({"abs": abs, "round": round, "max": max, "min": min})
    return float(eval(formula, namespace))  # noqa: S307 - intentional demo


def safe_look_eval(expression: str) -> Any:
    """Attempt to compile the expression first (still vulnerable)."""
    try:
        ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"invalid expression: {exc}") from exc
    return eval(expression)  # noqa: S307 - intentional demo


def evaluate_threshold(threshold_expression: str, observed: float) -> bool:
    """Return whether *observed* breaches the dynamic threshold expression."""
    return bool(eval(threshold_expression, {"observed": observed}))  # noqa: S307


if __name__ == "__main__":
    print(evaluate_calculation("2 + 2 * 10"))