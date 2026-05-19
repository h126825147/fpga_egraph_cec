from __future__ import annotations

from ..ir.circuit import Circuit
from ..ir.node import Node
from .egglog_model import Bit


def circuit_to_egglog(circuit: Circuit) -> Bit:
    node_map: dict[int, Bit] = {}

    # inputs
    for nid in getattr(circuit, "inputs", []):
        node_map[nid] = Bit.var(f"in{nid}")

    # nodes
    nodes = getattr(circuit, "nodes", {})
    if isinstance(nodes, dict):
        node_items = nodes.items()
    else:
        node_items = [(getattr(n, "id", None), n) for n in nodes]

    # recursive builder
    def build(nid: int) -> Bit:
        if nid in node_map:
            return node_map[nid]

        node = nodes.get(nid)
        if node is None:
            node_map[nid] = Bit.var(f"out{nid}")
            return node_map[nid]

        if not isinstance(node, Node):
            node_map[nid] = Bit.var(f"out{nid}")
            return node_map[nid]

        op = (node.op or "").upper()
        args = [build(a) for a in node.args]

        if op == "INPUT":
            expr = Bit.var(node.name or f"in{nid}")
        elif op in {"AND", "&"} and len(args) == 2:
            expr = args[0] & args[1]
        elif op in {"OR", "|"} and len(args) == 2:
            expr = args[0] | args[1]
        elif op in {"XOR", "^"} and len(args) == 2:
            expr = args[0] ^ args[1]
        elif op in {"NOT", "~"} and len(args) == 1:
            expr = ~args[0]
        else:
            expr = Bit.var(f"n{nid}")

        node_map[nid] = expr
        return expr

    outputs = list(getattr(circuit, "outputs", []))
    if not outputs:
        return Bit.var("empty")

    # AIGER output may point to node ids
    root_id = outputs[0]
    return build(root_id)