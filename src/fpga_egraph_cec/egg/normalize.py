from ..ir.circuit import Circuit
from ..ir.node import Node


def normalize_circuit(circuit: Circuit) -> Circuit:
    """
    Placeholder normalization:
    - keep structure
    - annotate levels
    - canonicalize simple commutative ordering
    """
    out = Circuit(name=circuit.name + "_norm")
    for nid in circuit.topological_order():
        n = circuit.nodes[nid]
        args = tuple(sorted(n.args)) if n.op in {"AND", "OR", "XOR"} else n.args
        out.add_node(Node(
            id=nid,
            op=n.op,
            args=args,
            name=n.name,
            src=n.src,
            level=n.level,
            attrs=dict(n.attrs),
        ))
    out.inputs = list(circuit.inputs)
    out.outputs = list(circuit.outputs)
    return out