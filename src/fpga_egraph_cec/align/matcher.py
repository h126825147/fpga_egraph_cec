from .signature import node_signature
from ..ir.circuit import Circuit


def candidate_pairs(ca: Circuit, cb: Circuit) -> list[tuple[int, int]]:
    sig_to_a = {}
    for nid in ca.nodes:
        sig_to_a.setdefault(node_signature(ca, nid), []).append(nid)

    pairs = []
    for nid in cb.nodes:
        sig = node_signature(cb, nid)
        if sig in sig_to_a:
            for aid in sig_to_a[sig]:
                pairs.append((aid, nid))
    return pairs