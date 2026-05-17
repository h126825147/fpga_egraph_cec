from __future__ import annotations

from pathlib import Path
import argparse
import csv
import json
import time
import yaml

from fpga_egraph_cec.bench.loader import load_benchmarks
from fpga_egraph_cec.exp.runner import run_experiment


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True, help="Path to configs/exp_default.yaml")
    ap.add_argument(
        "--group",
        default="main",
        choices=["smoke", "alignment", "main", "all"],
        help="Benchmark group to run",
    )
    ap.add_argument(
        "--benchmarks",
        default=None,
        help="Optional path to benchmarks.yaml; default: <bench_root>/benchmarks.yaml",
    )
    args = ap.parse_args()

    cfg_path = Path(args.config)
    cfg = yaml.safe_load(cfg_path.read_text())

    bench_yaml = Path(args.benchmarks) if args.benchmarks else Path(cfg["bench_root"]) / "benchmarks.yaml"
    cases = load_benchmarks(str(bench_yaml))

    if args.group != "all":
        cases = [c for c in cases if c.group == args.group]

    out_root = Path(cfg.get("output_root", "data/results"))
    out_root.mkdir(parents=True, exist_ok=True)

    t0 = time.time()
    results = run_experiment(cases, cfg)
    elapsed = time.time() - t0

    json_path = out_root / f"batch_{args.group}.json"
    csv_path = out_root / f"batch_{args.group}.csv"

    json_path.write_text(json.dumps({
        "group": args.group,
        "elapsed_sec": elapsed,
        "results": results,
    }, indent=2, ensure_ascii=False))

    if results:
        with csv_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(results[0].keys()))
            writer.writeheader()
            writer.writerows(results)

    print(f"[OK] group={args.group} cases={len(cases)} elapsed_sec={elapsed:.3f}")
    print(f"[OK] json={json_path}")
    if results:
        print(f"[OK] csv={csv_path}")


if __name__ == "__main__":
    main()