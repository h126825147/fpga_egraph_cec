from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Term:
    op: str
    args: tuple[Any, ...] = ()
    value: Any | None = None

    def __str__(self) -> str:
        if self.op == "CONST":
            return str(self.value)
        if self.op == "INPUT":
            return f"in({self.value})"
        if not self.args:
            return self.op
        return f"{self.op}({', '.join(map(str, self.args))})"