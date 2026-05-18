from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Tuple


@dataclass(frozen=True)
class ExprRef:
    id: int
    op: str
    args: Tuple[int, ...] = ()
    value: Any | None = None
    repr: str = ""


@dataclass(frozen=True)
class ExprNode:
    op: str
    args: Tuple["ExprNode", ...] = ()
    value: Any | None = None

    def __str__(self) -> str:
        if self.op == "CONST":
            return str(self.value)
        if self.op == "INPUT":
            return f"in({self.value})"
        if not self.args:
            return self.op
        return f"{self.op}({', '.join(map(str, self.args))})"