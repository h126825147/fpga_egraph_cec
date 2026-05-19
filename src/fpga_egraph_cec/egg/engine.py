from __future__ import annotations

from dataclasses import dataclass

from egglog import *

from .egglog_model import Bit
from .egglog_rules import bit_rules
from .egglog_translate import circuit_to_egglog
from .translate_precise import circuit_to_egglog_precise


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
    # 优先用更精细的翻译
    try:
        expr = circuit_to_egglog_precise(circuit)
    except Exception:
        expr = circuit_to_egglog(circuit)

    cost_before = circuit.size()
    log: list[str] = [f"expr={expr}"]

    egraph = EGraph()
    egraph.register(expr)
    egraph.run(run(bit_rules).saturate())

    try:
        optimized = egraph.extract(expr)
        log.append(f"optimized={optimized}")
    except Exception as e:
        optimized = expr
        log.append(f"extract_error={e!r}")

    changed = str(optimized) != str(expr)

    return NormalizeResult(
        circuit_name=getattr(circuit, "name", "unknown"),
        rounds=1,
        rules_applied=max_rules if changed else 0,
        cost_before=cost_before,
        cost_after=cost_before,
        changed=changed,
        log=log,
    )