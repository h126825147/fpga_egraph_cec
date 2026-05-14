from dataclasses import dataclass, field
from typing import Tuple, Dict, Any

@dataclass(frozen=True)
class Node:
    id: int
    op: str
    args: Tuple[int, ...]
    name: str | None = None
    src: str | None = None   # "A" / "B"
    level: int = 0
    attrs: Dict[str, Any] = field(default_factory=dict)