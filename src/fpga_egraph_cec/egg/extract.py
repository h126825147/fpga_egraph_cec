from __future__ import annotations


def extract_best_expr(egraph, root) -> object:
    """
    Minimal best-expression extraction placeholder.

    For now:
    - return the root expression unchanged
    - later replace with true egglog extraction
    """
    if root is None:
        raise ValueError("root expression is required")
    return root