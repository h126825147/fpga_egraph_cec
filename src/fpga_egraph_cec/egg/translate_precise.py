from __future__ import annotations

from collections.abc import Iterable

from ..ir.circuit import Circuit
from ..ir.node import Node
from .egglog_model import Bit


def _is_const_like(op: str) -> bool:
    op = op.upper()
    return op in {"CONST", "0", "1", "TRUE", "FALSE", "VCC", "GND"}


def _const_bit(node: Node) -> Bit:
    name = (getattr(node, "name", "") or "").lower()
    op = (getattr(node, "op", "") or "").upper()
    if "1" in name or op in {"1", "TRUE", "VCC"}:
        return Bit(1)
    return Bit(0)


def _get_node_iter(circuit: Circuit) -> Iterable[Node]:
    node_container = getattr(circuit, "nodes", None)
    if node_container is None:
        return []
    if isinstance(node_container, dict):
        return node_container.values()
    return node_container


def circuit_to_egglog_precise(circuit: Circuit) -> Bit:
    """
    A more precise translation from Circuit/Node to egglog Bit expressions.

    Strategy:
    - build mapping from node id to Bit
    - inputs become Bit.var(inX)
    - common gates map to egglog operators
    - unknown nodes keep symbolic placeholders but preserve dependencies where possible
    """
    node_map: dict[int, Bit] = {}

    # 1) inputs
    for nid in getattr(circuit, "inputs", []):
        node_map[nid] = Bit.var(f"in{nid}")

    # 2) nodes in iteration order
    for node in _get_node_iter(circuit):
        if not isinstance(node, Node):
            continue

        nid = getattr(node, "id", None)
        if nid is None:
            continue

        op = (getattr(node, "op", "") or "").upper()
        args_ids = tuple(getattr(node, "args", ()) or ())
        arg_terms = [node_map.get(a, Bit.var(f"n{a}")) for a in args_ids]

        # explicit input-like node
        if op == "INPUT":
            node_map[nid] = Bit.var(getattr(node, "name", None) or f"in{nid}")
            continue

        # constants
        if _is_const_like(op):
            node_map[nid] = _const_bit(node)
            continue

        # unary
        if op in {"NOT", "~", "INV"} and len(arg_terms) == 1:
            node_map[nid] = ~arg_terms[0]
            continue

        # binary
        if op in {"AND", "&", "AIG_AND"} and len(arg_terms) == 2:
            node_map[nid] = arg_terms[0] & arg_terms[1]
            continue

        if op in {"OR", "|"} and len(arg_terms) == 2:
            node_map[nid] = arg_terms[0] | arg_terms[1]
            continue

        if op in {"XOR", "^"} and len(arg_terms) == 2:
            node_map[nid] = arg_terms[0] ^ arg_terms[1]
            continue

        # ternary mux
        if op in {"MUX", "ITE", "SEL"} and len(arg_terms) == 3:
            # 你当前的 bit_rules 里有 mux 规则，但 Bit 类里还没 mux 方法
            # 这里先用表达式字符串兜底，后续如果你加 mux 运算符再替换
            node_map[nid] = Bit.var(f"mux_{nid}")
            continue

        # general fallback: preserve dependency as much as possible
        if arg_terms:
            # 组合成一个可追踪的变量名，避免全部塌成 outXXX
            dep_sig = "_".join(str(a).replace("Bit.var(", "").replace(")", "") for a in args_ids[:3])
            node_map[nid] = Bit.var(f"n{nid}_{dep_sig}")
        else:
            node_map[nid] = Bit.var(f"n{nid}")

    # 3) outputs
    outputs = list(getattr(circuit, "outputs", []))
    if not outputs:
        return Bit.var("empty")

    out_terms = [node_map.get(oid, Bit.var(f"out{oid}")) for oid in outputs]

    # single root preferred
    if len(out_terms) == 1:
        return out_terms[0]

    # multi-output: keep first output for v1, but include a merged debug label
    return out_terms[0]