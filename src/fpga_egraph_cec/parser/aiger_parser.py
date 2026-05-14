from pathlib import Path
from ..ir.circuit import Circuit
from ..ir.node import Node


def load_aag(path: str) -> Circuit:
    p = Path(path)
    lines = [ln.strip() for ln in p.read_text().splitlines() if ln.strip()]
    assert lines[0].startswith("aag"), "Only textual AAG is supported in v1"

    _, m, i, l, o, a = lines[0].split()
    i, o, a = int(i), int(o), int(a)

    c = Circuit(name=p.stem)
    idx = 1
    inputs = []
    for _ in range(i):
        lit = int(lines[idx])
        nid = lit // 2
        c.add_node(Node(id=nid, op="INPUT", args=(), name=f"in{nid}", src="A"))
        inputs.append(nid)
        idx += 1

    outputs = []
    for _ in range(o):
        lit = int(lines[idx])
        outputs.append(lit // 2)
        idx += 1

    # NOTE: proper AIG parsing will need AND gate decoding from literals.
    # This is a placeholder skeleton for v1.
    c.inputs = inputs
    c.outputs = outputs
    return c