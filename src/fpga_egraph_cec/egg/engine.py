from __future__ import annotations

from dataclasses import dataclass

from .expr import ExprNode
from .translate import circuit_to_expr
from .saturate import saturate


@dataclass
class NormalizeResult:
    circuit_name: str
    rounds: int
    rules_applied: int
    cost_before: int
    cost_after: int
    changed: bool
    log: list[str]


def run_egglog_normalize(circuit, max_rounds: int = 8, max_rules: int = 50) -> NormalizeResult:
    """
    Minimal egglog assembly layer:
    1) translate Circuit -> ExprNode
    2) saturate
    3) return summary

    This is still not a true egglog backend, but it is the correct integration layer
    for the next step.
    """
    expr = circuit_to_expr(circuit)
    sat = saturate(expr, max_rounds=max_rounds, max_rules=max_rules)

    cost_before = circuit.size()
    cost_after = circuit.size()

    return NormalizeResult(
        circuit_name=getattr(circuit, "name", "unknown"),
        rounds=sat.rounds,
        rules_applied=sat.rules_applied,
        cost_before=cost_before,
        cost_after=cost_after,
        changed=sat.changed,
        log=sat.log,
    )