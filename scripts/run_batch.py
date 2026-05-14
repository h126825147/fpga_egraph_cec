from pathlib import Path
import argparse
import json
import yaml

from fpga_egraph_cec.bench.loader import load_benchmarks
from fpga_egraph_cec.exp.runner import run_experiment


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    args = ap.parse_args()

    cfg = yaml.safe_load(Path(args.config).read_text())
    cases = load_benchmarks(Path(cfg["bench_root"]) / "benchmarks.yaml")
    run_experiment(cases, cfg)


if __name__ == "__main__":
    main()