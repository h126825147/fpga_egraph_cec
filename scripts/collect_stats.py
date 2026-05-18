from __future__ import annotations

from pathlib import Path
import argparse
import csv
import json
from statistics import mean, median
from typing import Any


def load_results(path: Path) -> list[dict[str, Any]]:
    if path.suffix.lower() == ".json":
        obj = json.loads(path.read_text())
        if isinstance(obj, dict) and "results" in obj:
            return obj["results"] or []
        if isinstance(obj, list):
            return obj
        return []

    if path.suffix.lower() == ".csv":
        with path.open("r", newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))

    raise ValueError(f"Unsupported input type: {path.suffix}")


def to_float(v: Any, default: float = 0.0) -> float:
    try:
        if v is None or v == "":
            return default
        return float(v)
    except Exception:
        return default


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not rows:
        return {
            "cases": 0,
            "equivalent": 0,
            "not_equivalent": 0,
            "timeout": 0,
            "unknown": 0,
        }

    statuses = [str(r.get("verify_status", "unknown")) for r in rows]
    circuits = [to_float(r.get("circuit_size")) for r in rows]
    align_scores = [to_float(r.get("alignment_score")) for r in rows]
    standard_miters = [to_float(r.get("standard_miter_size")) for r in rows]
    aligned_miters = [to_float(r.get("aligned_miter_size")) for r in rows]
    verify_times = [to_float(r.get("verify_time")) for r in rows]

    return {
        "cases": len(rows),
        "equivalent": sum(s == "equivalent" for s in statuses),
        "not_equivalent": sum(s == "not_equivalent" for s in statuses),
        "timeout": sum(s == "timeout" for s in statuses),
        "unknown": sum(s == "unknown" for s in statuses),
        "avg_circuit_size": mean(circuits),
        "med_circuit_size": median(circuits),
        "avg_alignment_score": mean(align_scores),
        "avg_standard_miter_size": mean(standard_miters),
        "avg_aligned_miter_size": mean(aligned_miters),
        "avg_verify_time_sec": mean(verify_times),
    }


def group_summary(rows: list[dict[str, Any]], key: str = "group") -> dict[str, Any]:
    groups: dict[str, list[dict[str, Any]]] = {}
    for r in rows:
        g = str(r.get(key, "unknown"))
        groups.setdefault(g, []).append(r)

    return {g: summarize(v) for g, v in groups.items()}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Path to batch result JSON/CSV")
    ap.add_argument("--group-by", default="group", help="Field for group summary")
    args = ap.parse_args()

    path = Path(args.input)
    rows = load_results(path)

    summary = summarize(rows)
    grouped = group_summary(rows, key=args.group_by)

    print("=== OVERALL SUMMARY ===")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    print("\n=== GROUP SUMMARY ===")
    print(json.dumps(grouped, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()