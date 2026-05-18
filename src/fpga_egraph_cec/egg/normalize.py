from __future__ import annotations

from .engine import run_egglog_normalize


def normalize_circuit(circuit, config: dict | None = None):
    config = config or {}
    use_egglog = bool(config.get("use_egglog", True))
    max_rounds = int(config.get("max_rounds", 8))
    max_rules = int(config.get("max_rules", 50))

    if use_egglog:
        res = run_egglog_normalize(circuit, max_rounds=max_rounds, max_rules=max_rules)
        setattr(circuit, "_normalize_result", res)
        return circuit

    return circuit