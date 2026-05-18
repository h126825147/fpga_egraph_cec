from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .expr import ExprNode


@dataclass
class EClass:
    id: int
    nodes: List[ExprNode] = field(default_factory=list)


@dataclass
class EGraphModel:
    classes: Dict[int, EClass] = field(default_factory=dict)
    root: Optional[int] = None
    next_id: int = 0

    def add(self, node: ExprNode) -> int:
        eid = self.next_id
        self.next_id += 1
        self.classes[eid] = EClass(id=eid, nodes=[node])
        if self.root is None:
            self.root = eid
        return eid

    def add_alias(self, target: int, source: int) -> None:
        if target not in self.classes or source not in self.classes:
            return
        self.classes[target].nodes.extend(self.classes[source].nodes)
        del self.classes[source]

    def size(self) -> int:
        return len(self.classes)