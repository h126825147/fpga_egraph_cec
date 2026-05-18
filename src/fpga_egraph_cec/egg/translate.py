from __future__ import annotations

from ..ir.circuit import Circuit
from ..ir.node import Node
from .circuit_terms import Term


def circuit_to_expr(circuit: Circuit) -> Term:
    """
    Best-effort translation from Circuit IR to a symbolic term tree.
    """
    node_map: dict[int, Term] = {}

    inputs = list(getattr(circuit, "inputs", []))
    outputs = list(getattr(circuit, "outputs", []))

    # create explicit input terms
    for nid in inputs:
        node_map[nid] = Term(op="INPUT", value=nid)

    # translate node objects if available
    if hasattr(circuit, "nodes"):
        nodes_obj = getattr(circuit, "nodes")
        if isinstance(nodes_obj, dict):
            node_iter = nodes_obj.values()
        else:
            node_iter = nodes_obj

        for node in node_iter:
            if not isinstance(node, Node):
                continue
            args = tuple(node_map.get(a, Term(op="VAR", value=a)) for a in getattr(node, "args", ()))
            node_map[node.id] = Term(op=node.op, args=args)

    # build output terms
    out_terms = []
    for oid in outputs:
        out_terms.append(node_map.get(oid, Term(op="VAR", value=oid)))

    if len(out_terms) == 1:
        return out_terms[0]
    return Term(op="TUPLE", args=tuple(out_terms))