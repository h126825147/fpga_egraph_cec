from .circuit import Circuit


def to_text(circuit: Circuit) -> str:
    lines = [f"circuit {circuit.name}"]
    lines.append(f"inputs: {circuit.inputs}")
    lines.append(f"outputs: {circuit.outputs}")
    for nid in circuit.topological_order():
        n = circuit.nodes[nid]
        lines.append(f"{n.id}: {n.op} {list(n.args)} src={n.src} lvl={n.level}")
    return "\n".join(lines)