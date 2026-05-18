from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .expr import ExprNode
from .rules import RULES, RewriteRule


@dataclass
class SaturationResult:
    rounds: int
    rules_applied: int
    before_repr: str
    after_repr: str
    changed: bool
    log: list[str]


def apply_simple_rules(expr: ExprNode, rules: List[RewriteRule]) -> tuple[ExprNode, int]:
    """
    Minimal placeholder reducer.
    For now this only demonstrates the pipeline and does not yet perform
    full symbolic rewriting.
    """
    # No real rewrite in v1; return as-is.
    return expr, 0


def saturate(expr: ExprNode, max_rounds: int = 8, max_rules: int = 50) -> SaturationResult:
    before = str(expr)
    current = expr
    total_rules = 0
    log: list[str] = [f"before={before}"]

    rounds = 0
    for r in range(max_rounds):
        rounds += 1
        current, applied = apply_simple_rules(current, RULES[:max_rules])
        total_rules += applied
        log.append(f"round={r} applied={applied} current={current}")
        if applied == 0:
            break

    after = str(current)
    changed = before != after
    return SaturationResult(
        rounds=rounds,
        rules_applied=total_rules,
        before_repr=before,
        after_repr=after,
        changed=changed,
        log=log,
    )