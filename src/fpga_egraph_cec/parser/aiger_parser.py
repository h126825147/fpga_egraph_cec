from __future__ import annotations

from pathlib import Path
from ..ir.circuit import Circuit
from ..ir.node import Node


def _read_aag_text(path: Path) -> list[str]:
    raw = path.read_bytes()

    # Try UTF-8 first, then latin-1 as a fallback.
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