from ..ir.circuit import Circuit
from ..ir.node import Node
from ..align.aligner import AlignmentResult


def build_miter(ca: Circuit, cb: Circuit) -> Circuit:
    m = Circuit(name=f"miter_{ca.name}_{cb.name}")
    # placeholder: use output XORs and a final OR
    out_nodes = []
    nid = 1
    for _ in range(min(len(ca.outputs), len(cb.outputs))):
        x = Node(id=nid, op="XOR", args=(), name=None)
        m.add_node(x)
        out_nodes.append(nid)
        nid += 1
    if out_nodes:
        root = Node(id=nid, op="OR", args=tuple(out_nodes))
        m.add_node(root)
        m.outputs = [nid]
    return m


def build_aligned_miter(ca: Circuit, cb: Circuit, alignment: AlignmentResult) -> Circuit:
    # v1: same as standard miter, but intended to use alignment for node replacement later
    return build_miter(ca, cb)