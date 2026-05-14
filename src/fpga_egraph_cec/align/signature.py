from ..ir.circuit import Circuit


def node_signature(circuit: Circuit, nid: int) -> tuple:
    n = circuit.nodes[nid]
    return (
        n.op,
        len(n.args),
        tuple(sorted(n.args)) if n.op in {"AND", "OR", "XOR"} else n.args,
        n.level,
        n.src,
        bool(nid in circuit.outputs),
    )