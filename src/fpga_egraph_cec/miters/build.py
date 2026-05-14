def build_miter(ca: Circuit, cb: Circuit) -> Circuit:
    """Build a standard equivalence miter."""
    # Create a new circuit for the miter
    miter = Circuit()

    # Add nodes from both circuits to the miter
    for node in ca.nodes.values():
        miter.add_node(node)
    for node in cb.nodes.values():
        miter.add_node(node)

    # Create an XOR node to compare the outputs of both circuits
    output_a = ca.get_output_node()
    output_b = cb.get_output_node()
    xor_node = Node(op="xor", children=[output_a.id, output_b.id])
    miter.add_node(xor_node)

    # The output of the miter is the XOR node
    miter.set_output(xor_node.id)

    return miter


def build_aligned_miter(ca: Circuit, cb: Circuit, alignment: AlignmentResult) -> Circuit:
    """Build an alignment-aware miter."""
    # Create a new circuit for the miter
    miter = Circuit()

    # Add nodes from both circuits to the miter, applying the alignment mapping
    for node in ca.nodes.values():
        miter.add_node(node)
    for node in cb.nodes.values():
        mapped_id = alignment.mapping.get(node.id)
        if mapped_id is not None:
            # If there is a mapping, use the mapped node from ca
            miter.add_node(ca.nodes[mapped_id])
        else:
            # Otherwise, add the original node from cb
            miter.add_node(node)

    # Create an XOR node to compare the outputs of both circuits
    output_a = ca.get_output_node()
    output_b = cb.get_output_node()
    xor_node = Node(op="xor", children=[output_a.id, output_b.id])
    miter.add_node(xor_node)

    # The output of the miter is the XOR node
    miter.set_output(xor_node.id)

    return miter