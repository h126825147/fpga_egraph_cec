from __future__ import annotations

from ..ir.circuit import Circuit
from ..ir.node import Node
from .expr import ExprNode


def circuit_to_expr(circuit: Circuit) -> ExprNode:
    """
    Minimal translation from Circuit IR to ExprNode.
    """
    node_map: dict[int, ExprNode] = {}

    # inputs
    for nid in getattr(circuit, "inputs", []):
        node_map[nid] = ExprNode(op="INPUT", value=nid)

    # best-effort translation of nodes
    for node in getattr(circuit, "nodes", {}).values() if hasattr(circuit, "nodes") else []:
        if not isinstance(node, Node):
            continue
        args = tuple(node_map.get(a, ExprNode(op="VAR", value=a)) for a in node.args)
        node_map[node.id] = ExprNode(op=node.op, args=args)

    # outputs
    outs = []
    for oid in getattr(circuit, "outputs", []):
        outs.append(node_map.get(oid, ExprNode(op="VAR", value=oid)))

    if len(outs) == 1:
        return outs[0]
    return ExprNode(op="TUPLE", args=tuple(outs))