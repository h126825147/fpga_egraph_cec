from dataclasses import dataclass, field
from collections import defaultdict, deque
from .node import Node


@dataclass
class Circuit:
    name: str
    nodes: dict[int, Node] = field(default_factory=dict)
    inputs: list[int] = field(default_factory=list)
    outputs: list[int] = field(default_factory=list)

    def add_node(self, node: Node) -> None:
        self.nodes[node.id] = node

    def fanin(self, nid: int) -> tuple[int, ...]:
        return self.nodes[nid].args

    def fanout(self, nid: int) -> list[int]:
        outs = []
        for oid, node in self.nodes.items():
            if nid in node.args:
                outs.append(oid)
        return outs

    def topological_order(self) -> list[int]:
        indeg = defaultdict(int)
        graph = defaultdict(list)
        for nid, node in self.nodes.items():
            for a in node.args:
                graph[a].append(nid)
                indeg[nid] += 1

        q = deque([nid for nid in self.nodes if indeg[nid] == 0])
        order = []
        while q:
            u = q.popleft()
            order.append(u)
            for v in graph[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)
        return order

    def size(self) -> int:
        return len(self.nodes)

    def depth(self) -> int:
        levels = {}
        for nid in self.topological_order():
            node = self.nodes[nid]
            if not node.args:
                levels[nid] = 0
            else:
                levels[nid] = 1 + max(levels[a] for a in node.args)
        return max((levels[o] for o in self.outputs), default=0)