from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import subprocess
import tempfile
import re

from .loader import BenchmarkCase


def _run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def detect_verilog_top(src: Path) -> str:
    """
    Very small heuristic:
    - collect all module definitions
    - collect all module instantiations
    - choose the module that is defined but never instantiated
    - fallback to the first module definition
    """
    text = src.read_text(errors="ignore")

    # module foo (...);
    mod_defs = re.findall(r"^\s*module\s+([A-Za-z_][A-Za-z0-9_$]*)\b", text, flags=re.M)
    if not mod_defs:
        raise ValueError(f"No module definition found in {src}")

    # instantiations: foo u0 (...);
    # remove definition lines first to reduce false matches
    body = re.sub(r"^\s*module\s+.*?$", "", text, flags=re.M)
    body = re.sub(r"^\s*endmodule\s*$", "", body, flags=re.M)

    instantiated = set(re.findall(r"^\s*([A-Za-z_][A-Za-z0-9_$]*)\s+[A-Za-z_][A-Za-z0-9_$]*\s*\(", body, flags=re.M))

    for m in mod_defs:
        if m not in instantiated:
            return m

    return mod_defs[0]


def convert_to_aag(case: BenchmarkCase, out_dir: str | Path) -> BenchmarkCase:
    """
    Convert Verilog/VHDL benchmark to textual AAG.
    Requires yosys in PATH.
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    src = Path(case.path)
    if case.kind == "aiger":
        return case

    out_aag = out_dir / f"{case.name}.aag"

    if src.suffix.lower() in {".v", ".sv"}:
        # Verilog -> AIGER
        # 这里用 yosys 的标准流程：read_verilog -> proc -> opt -> aigmap -> write_aiger
        top = detect_verilog_top(src)
        script = (
            f"read_verilog {src}; "
            f"hierarchy -top {top}; "
            f"proc; opt; aigmap; "
            f"write_aiger -ascii {out_aag}"
        )
        _run(["yosys", "-p", script])

    elif src.suffix.lower() in {".vhd", ".vhdl"}:
        # VHDL -> AIGER
        # 若你已安装 ghdl + yosys plugin，可用下面路线；
        # 如果当前环境还没有 ghdl-yosys，请先把 VHDL 预处理为 Verilog 或 AIGER。
        # script = f"ghdl {src}; synth; opt; aigmap; write_aiger {out_aag}"
        # _run(["yosys", "-p", script])

        raise NotImplementedError(
            "VHDL conversion is not enabled yet in this minimal version. "
            "Please convert VHDL benchmarks to Verilog/AAG first."
        )

    else:
        raise ValueError(f"Unsupported benchmark source format: {src.suffix}")

    return replace(case, kind="aiger", aig_path=str(out_aag), path=str(out_aag))