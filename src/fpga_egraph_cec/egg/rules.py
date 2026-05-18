from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RewriteRule:
    name: str
    lhs: str
    rhs: str


RULES = [
    RewriteRule("and_one", "a & 1", "a"),
    RewriteRule("and_zero", "a & 0", "0"),
    RewriteRule("or_zero", "a | 0", "a"),
    RewriteRule("or_one", "a | 1", "1"),
    RewriteRule("xor_zero", "a ^ 0", "a"),
    RewriteRule("xor_one", "a ^ 1", "~a"),
    RewriteRule("double_not", "~~a", "a"),
    RewriteRule("and_idem", "a & a", "a"),
    RewriteRule("or_idem", "a | a", "a"),
    RewriteRule("xor_self", "a ^ a", "0"),
    RewriteRule("de_morgan_and", "~(a & b)", "~a | ~b"),
    RewriteRule("de_morgan_or", "~(a | b)", "~a & ~b"),
    RewriteRule("mux_same", "mux(s, a, a)", "a"),
    RewriteRule("mux_true", "mux(1, a, b)", "a"),
    RewriteRule("mux_false", "mux(0, a, b)", "b"),
    RewriteRule("absorb_and", "a & (a | b)", "a"),
    RewriteRule("absorb_or", "a | (a & b)", "a"),
    RewriteRule("xor_neg", "a ^ ~a", "1"),
    RewriteRule("xor_neg2", "~a ^ a", "1"),
    RewriteRule("xor_assoc1", "(a ^ b) ^ b", "a"),
    RewriteRule("xor_assoc2", "a ^ (a ^ b)", "b"),
]