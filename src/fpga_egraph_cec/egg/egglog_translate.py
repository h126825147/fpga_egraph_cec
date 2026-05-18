from __future__ import annotations

from ..ir.circuit import Circuit
from ..ir.node import Node
from .egglog_model import Bit


def circuit_to_egglog(circuit: Circuit) -> Bit:
    """
    Best-effort translation from internal Circuit IR to egglog Bit expressions.
    """
    node_map: dict[int, Bit] = {}

    # inputs
    for nid in getattr(circuit, "inputs", []):
        node_map[nid] = Bit.var(f"in{nid}")

    # nodes
    node_container = getattr(circuit, "nodes", None)
    if isinstance(node_container, dict):
        node_iter = node_container.values()
    elif node_container is None:
        node_iter = []
    else:
        node_iter = node_container

    for node in node_iter:
        if not isinstance(node, Node):
            continue

        args = [node_map.get(a, Bit.var(f"in{a}")) for a in getattr(node, "args", ())]
        op = getattr(node, "op", "").upper()

        if op in {"INPUT"}:
            node_map[node.id] = Bit.var(node.name or f"in{node.id}")
        elif op in {"NOT", "~"} and len(args) == 1:
            node_map[node.id] = ~args[0]
        elif op in {"AND", "&"} and len(args) == 2:
            node_map[node.id] = args[0] & args[1]
        elif op in {"OR", "|"} and len(args) == 2:
            node_map[node.id] = args[0] | args[1]
        elif op in {"XOR", "^"} and len(args) == 2:
            node_map[node.id] = args[0] ^ args[1]
        else:
            # fallback：保留变量，不丢结构
            node_map[node.id] = Bit.var(f"n{node.id}")

    outputs = getattr(circuit, "outputs", [])
    if not outputs:
        return Bit.var("empty")

    # v1 只处理单 root，多个输出时先返回第一个
    root = outputs[0]
    return node_map.get(root, Bit.var(f"out{root}"))