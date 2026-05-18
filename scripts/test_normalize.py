from __future__ import annotations

from pathlib import Path
import yaml

from fpga_egraph_cec.bench.loader import load_benchmarks
from fpga_egraph_cec.bench.prepare import convert_to_aag
from fpga_egraph_cec.parser.aiger_parser import load_aag
from fpga_egraph_cec.egg.normalize import normalize_circuit


def main() -> None:
    cfg = yaml.safe_load(Path("configs/exp_default.yaml").read_text())
    cases = load_benchmarks("data/raw/benchmarks/benchmarks.yaml")
    case = cases[0]

    yosys_bin = cfg.get("yosys", {}).get("binary", "yosys")
    prep = convert_to_aag(case, "data/results/prepared-test", yosys_bin=yosys_bin)
    circuit = load_aag(prep.path)
    norm = normalize_circuit(circuit, cfg.get("normalize", {}))

    res = getattr(norm, "_normalize_result", None)
    print("name:", case.name)
    print("size:", norm.size())
    print("normalize_result:", res)

    if res:
        print("logs:")
        for line in res.log:
            print("  ", line)


if __name__ == "__main__":
    main()