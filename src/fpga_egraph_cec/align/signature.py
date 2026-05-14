def node_signature(circuit: Circuit, nid: int) -> tuple:
    """Return a hashable signature for alignment."""
    node = circuit.nodes[nid]
    if node.op == "input":
        return ("input", node.name)
    elif node.op in {"and", "or", "not"}:
        child_sigs = tuple(sorted(node_signature(circuit, child) for child in node.children))
        return (node.op, child_sigs)
    else:
        raise ValueError(f"Unknown operation: {node.op}")