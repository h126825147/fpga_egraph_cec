@dataclass
class BenchmarkCase:
    name: str
    path: str
    kind: str          # "aiger", "blif"
    category: str      # "epfl", "abc", "arith", "custom"
    tags: list[str]

def load_benchmarks(config_path: str) -> list[BenchmarkCase]:
    ...