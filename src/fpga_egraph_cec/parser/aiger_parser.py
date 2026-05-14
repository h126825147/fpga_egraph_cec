def load_aiger(path: str) -> Circuit:
    """Parse AIGER/AIG and return a Circuit."""
    with open(path, "r") as f:
        lines = f.readlines()

    # Parse header
    header = lines[0].strip().split()
    assert header[0] == "aag", "Only AIGER ASCII format is supported."
    M, I, L, O, A = map(int, header[1:6])

    circuit = Circuit(name=path)

    # Parse inputs
    for i in range(1, I + 1):
        lit = int(lines[i].strip())
        nid = lit // 2
        circuit.inputs.append(nid)
        circuit.add_node(Node(id=nid, op="input", args=()))

    # Parse latches (ignored for combinational circuits)
    for i in range(I + 1, I + L + 1):
        pass

    # Parse outputs
    for i in range(I + L + 1, I + L + O + 1):
        lit = int(lines[i].strip())
        nid = M + len(circuit.outputs) + 1
        circuit.outputs.append(nid)
        circuit.add_node(Node(id=nid, op="output", args=(lit // 2,)))

    # Parse AND gates
    for i in range(I + L + O + 1, I + L + O + A + 1):
        parts = lines[i].strip().split()
        assert len(parts) == 3
        lhs_lit, rhs0_lit, rhs1_lit = map(int, parts)
        nid = lhs_lit // 2
        rhs0_nid = rhs0_lit // 2
        rhs1_nid = rhs1_lit // 2
        circuit.add_node(Node(id=nid, op="and", args=(rhs0_nid, rhs1_nid)))

    return circuit