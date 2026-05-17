from dataclasses import dataclass, field
from pathlib import Path
import yaml


@dataclass
class BenchmarkCase:
    name: str
    path: str
    kind: str
    category: str
    tags: list[str] = field(default_factory=list)
    group: str = "main"
    expected_equal: bool = True
    source: str | None = None


def load_benchmarks(config_path: str) -> list[BenchmarkCase]:
    cfg = yaml.safe_load(Path(config_path).read_text())
    cases = []
    for item in cfg.get("benchmarks", []):
        cases.append(BenchmarkCase(
            name=item["name"],
            path=item["path"],
            kind=item.get("kind", "aiger"),
            category=item.get("category", "custom"),
            tags=item.get("tags", []),
        ))
    return cases