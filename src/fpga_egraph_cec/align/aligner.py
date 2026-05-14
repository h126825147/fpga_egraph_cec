from dataclasses import dataclass
from ..ir.circuit import Circuit
from .matcher import candidate_pairs


@dataclass
class AlignmentResult:
    mapping: dict[int, int]
    shared_classes: dict[int, int]
    score: float
    stats: dict


def align_circuits(ca: Circuit, cb: Circuit) -> AlignmentResult:
    pairs = candidate_pairs(ca, cb)
    mapping = {}
    used_b = set()

    for a, b in pairs:
        if a not in mapping and b not in used_b:
            mapping[a] = b
            used_b.add(b)

    coverage = len(mapping) / max(1, min(len(ca.nodes), len(cb.nodes)))
    return AlignmentResult(
        mapping=mapping,
        shared_classes={},
        score=coverage,
        stats={
            "candidate_pairs": len(pairs),
            "matched_pairs": len(mapping),
            "coverage": coverage,
        },
    )