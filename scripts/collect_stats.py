from __future__ import annotations

from pathlib import Path
import argparse
import csv
import json
from statistics import mean


def load_results(path: Path) -> list[dict]:
    if path.suffix == ".json":
        obj = json.loads(path.read_text())
        return obj.get("results", [])
    if path.suffix == ".csv":
        with path.open("r", newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    raise ValueError(f"Unsupported file type: {path}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Path to batch_*.json or batch_*.csv")
    args = ap.parse_args()

    path = Path(args.input)
    rows = load_results(path)

    if not rows:
        print("No rows found.")
        return

    def to_float(v, default=0.0):
        try:
            return float(v)
        except Exception:
            return default

    summary = {
        "cases": len(rows),
        "avg_circuit_size": mean(to_float(r.get("circuit_size", 0)) for r in rows),
        "avg_circuit_depth": mean(to_float(r.get("circuit_depth", 0)) for r in rows),
        "avg_alignment_coverage": mean(to_float(r.get("alignment_coverage", 0)) for r in rows),
        "avg_verify_time": mean(to_float(r.get("verify_time", 0)) for r in rows),
    }

    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()