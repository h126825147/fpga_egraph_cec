from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class BenchmarkCase:
    name: str
    path: str
    kind: str = "aiger"          # "aiger", "verilog", "vhdl"
    category: str = "custom"     # "epfl", "abc", "arith", "custom"
    tags: list[str] = field(default_factory=list)
    group: str = "main"          # "smoke", "alignment", "main"
    expected_equal: bool = True
    source: str | None = None
    aig_path: str | None = None   # 预处理后生成的 AAG 路径
    meta: dict[str, Any] = field(default_factory=dict)


def load_benchmarks(config_path: str) -> list[BenchmarkCase]:
    cfg = yaml.safe_load(Path(config_path).read_text()) or {}
    cases: list[BenchmarkCase] = []

    for item in cfg.get("benchmarks", []):
        cases.append(
            BenchmarkCase(
                name=item["name"],
                path=item["path"],
                kind=item.get("kind", "aiger"),
                category=item.get("category", "custom"),
                tags=item.get("tags", []),
                group=item.get("group", "main"),
                expected_equal=bool(item.get("expected_equal", True)),
                source=item.get("source"),
                aig_path=item.get("aig_path"),
                meta={k: v for k, v in item.items()
                      if k not in {
                          "name", "path", "kind", "category", "tags",
                          "group", "expected_equal", "source", "aig_path"
                      }},
            )
        )

    return cases