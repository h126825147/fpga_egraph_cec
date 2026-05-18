from __future__ import annotations

from dataclasses import dataclass

from egglog import *

from .egglog_model import Bit
from .egglog_rules import bit_rules
from .egglog_translate import circuit_to_egglog


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
    expr = circuit_to_egglog(circuit)
    cost_before = circuit.size()
    log: list[str] = [f"expr={expr}"]

    egraph = EGraph()

    # 1) 先注册表达式
    egraph.register(expr)

    # 2) 再运行规则
    egraph.run(run(bit_rules).saturate())

    # 3) 提取结果
    try:
        optimized = egraph.extract(expr)
        log.append(f"optimized={optimized}")
    except Exception as e:
        optimized = expr
        log.append(f"extract_error={e!r}")

    cost_after = circuit.size()
    changed = str(optimized) != str(expr)

    return NormalizeResult(
        circuit_name=getattr(circuit, "name", "unknown"),
        rounds=1,
        rules_applied=max_rules if changed else 0,
        cost_before=cost_before,
        cost_after=cost_after,
        changed=changed,
        log=log,
    )