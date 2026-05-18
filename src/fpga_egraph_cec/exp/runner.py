from __future__ import annotations

from pathlib import Path
from typing import Any

from ..bench.loader import BenchmarkCase
from ..bench.prepare import convert_to_aag
from ..parser.aiger_parser import load_aag
from ..egg.normalize import normalize_circuit
from ..align.aligner import align_circuits
from ..miters.build import build_miter, build_aligned_miter
from ..verify.abc_runner import run_abc_verify


def run_experiment(cases: list[BenchmarkCase], config: dict[str, Any]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    prep_dir = Path(config.get("output_root", "data/results")) / "prepared"
    prep_dir.mkdir(parents=True, exist_ok=True)

    yosys_bin = config.get("yosys", {}).get("binary", "yosys") if config.get("yosys", {}).get("enabled", False) else None
    abc_bin = config.get("abc", {}).get("binary", "abc") if config.get("abc", {}).get("enabled", False) else "abc"
    abc_timeout = int(config.get("abc", {}).get("timeout_sec", config.get("timeout_sec", 300)))

    for case in cases:
        prepared_case = case
        if case.kind != "aiger":
            prepared_case = convert_to_aag(case, prep_dir, yosys_bin=yosys_bin)

        circuit = load_aag(prepared_case.path)
        norm = normalize_circuit(circuit, config.get("normalize", {}))

        aligned = align_circuits(norm, norm)
        standard_miter = build_miter(norm, norm)
        aligned_miter = build_aligned_miter(norm, norm, aligned)

        # 最小闭环：先用当前可用的 AIG 输入做 ABC 可执行性验证
        # 后续导出 miter 后，把这里换成 miter_path
        verify_res = run_abc_verify(
            prepared_case.path,
            timeout_sec=abc_timeout,
            abc_bin=abc_bin,
        )

        row = {
            "name": case.name,
            "group": case.group,
            "category": case.category,
            "kind": prepared_case.kind,
            "path": prepared_case.path,
            "aig_path": prepared_case.aig_path or prepared_case.path,
            "circuit_size": norm.size(),
            "alignment_score": getattr(aligned, "score", None),
            "standard_miter_size": standard_miter.size(),
            "aligned_miter_size": aligned_miter.size(),
            "verify_status": verify_res.status,
            "verify_time": verify_res.time_sec,
            "abc_returncode": verify_res.details.get("returncode"),
        }
        results.append(row)

        print(
            case.name,
            row["circuit_size"],
            row["alignment_score"],
            row["standard_miter_size"],
            row["aligned_miter_size"],
            row["verify_status"],
        )

    return results