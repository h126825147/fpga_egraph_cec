from __future__ import annotations

from pathlib import Path
import argparse
import yaml

from fpga_egraph_cec.bench.loader import load_benchmarks
from fpga_egraph_cec.bench.prepare import convert_to_aag


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--benchmarks", required=True, help="Path to benchmarks.yaml")
    ap.add_argument("--out-dir", default="data/raw/benchmarks/prepared", help="Output directory for AAG files")
    ap.add_argument(
        "--out-yaml",
        default="data/raw/benchmarks/benchmarks.prepared.yaml",
        help="Output YAML with aig_path filled in",
    )
    args = ap.parse_args()

    bench_yaml = Path(args.benchmarks)
    out_dir = Path(args.out_dir)
    out_yml = Path(args.out_yaml)

    cases = load_benchmarks(str(bench_yaml))
    prepared = []

    for case in cases:
        new_case = case
        if case.kind != "aiger":
            new_case = convert_to_aag(case, out_dir)

        item = {
            "name": new_case.name,
            "path": new_case.path,
            "kind": new_case.kind,
            "category": new_case.category,
            "group": new_case.group,
            "tags": new_case.tags,
            "expected_equal": new_case.expected_equal,
            "source": new_case.source,
        }
        if new_case.aig_path:
            item["aig_path"] = new_case.aig_path

        prepared.append(item)

    out_yml.parent.mkdir(parents=True, exist_ok=True)
    out_yml.write_text(yaml.safe_dump({"benchmarks": prepared}, sort_keys=False, allow_unicode=True))
    print(f"[OK] wrote {out_yml}")


if __name__ == "__main__":
    main()