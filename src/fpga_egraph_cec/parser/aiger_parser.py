from __future__ import annotations

from pathlib import Path

from ..ir.circuit import Circuit
from ..ir.node import Node


def _read_aag_text(path: Path) -> list[str]:
    raw = path.read_bytes()
    for encoding in ("utf-8", "latin-1"):
        try:
            text = raw.decode(encoding)
            lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
            if lines:
                return lines
        except UnicodeDecodeError:
            pass
    raise UnicodeDecodeError("aag", raw, 0, min(len(raw), 64), "unable to decode AAG file")


def load_aag(path: str) -> Circuit:
    p = Path(path)
    lines = _read_aag_text(p)
    assert lines[0].startswith("aag"), f"Only textual AAG is supported in v1, got header: {lines[0]!r}"

    _, m, i, l, o, a = lines[0].split()
    m, i, l, o, a = int(m), int(i), int(l), int(o), int(a)

    c = Circuit(name=p.stem)
    idx = 1

    # AIGER literal -> node id mapping
    lit_to_nid: dict[int, int] = {}
    nodes: dict[int, Node] = {}

    # 1) inputs
    inputs = []
    for k in range(i):
        lit = int(lines[idx])
        nid = lit // 2
        node = Node(id=nid, op="INPUT", args=(), name=f"in{nid}", src="A")
        nodes[nid] = node
        lit_to_nid[lit] = nid
        inputs.append(nid)
        idx += 1

    # 2) latches (not handled in v1)
    for _ in range(l):
        idx += 1

    # 3) outputs
    outputs: list[int] = []
    output_lits: list[int] = []
    for _ in range(o):
        lit = int(lines[idx])
        output_lits.append(lit)
        # output may refer to an internal node; resolve later
        outputs.append(lit)
        idx += 1

    # 4) AND gates
    # each AND line: lhs rhs0 rhs1
    # lhs is an even literal; rhs literals can be complemented
    for _ in range(a):
        lhs, rhs0, rhs1 = map(int, lines[idx].split())
        nid = lhs // 2

        # AIGER semantics:
        # lhs = 2*n
        # rhs literals may be complemented
        arg0 = rhs0 // 2
        arg1 = rhs1 // 2

        # store node with raw literal args first
        node = Node(id=nid, op="AND", args=(arg0, arg1), name=f"n{nid}", src="G")
        nodes[nid] = node
        lit_to_nid[lhs] = nid
        idx += 1

    # 5) Fix outputs to node ids if possible
    resolved_outputs: list[int] = []
    for lit in output_lits:
        if lit in lit_to_nid:
            resolved_outputs.append(lit_to_nid[lit])
        else:
            resolved_outputs.append(lit // 2)

    c.inputs = inputs
    c.outputs = resolved_outputs
    c.nodes = nodes  # make sure circuit keeps full node map
    return c