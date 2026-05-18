from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess
import time


@dataclass
class VerificationResult:
    status: str
    time_sec: float
    raw_output: str
    details: dict


def run_abc_verify(aig_path: str, timeout_sec: int = 300, abc_bin: str = "abc") -> VerificationResult:
    """
    Minimal ABC verification wrapper.

    Expected usage:
      - aig_path points to a valid AIG/AAG file
      - abc_bin points to the ABC executable
    """
    t0 = time.time()
    cmd = [abc_bin, "-c", f"read {aig_path}; strash; cec"]

    try:
        if not Path(aig_path).exists():
            return VerificationResult(
                status="input_not_found",
                time_sec=time.time() - t0,
                raw_output=f"Input file not found: {aig_path}",
                details={"cmd": cmd},
            )

        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_sec)
        out = (proc.stdout or "") + "\n" + (proc.stderr or "")

        low = out.lower()
        status = "unknown"
        if "networks are equivalent" in low or "equivalent" in low:
            status = "equivalent"
        elif "networks are not equivalent" in low or "not equivalent" in low:
            status = "not_equivalent"
        elif "timeout" in low:
            status = "timeout"

        return VerificationResult(
            status=status,
            time_sec=time.time() - t0,
            raw_output=out,
            details={"returncode": proc.returncode, "cmd": cmd},
        )

    except subprocess.TimeoutExpired as e:
        return VerificationResult(
            status="timeout",
            time_sec=time.time() - t0,
            raw_output=str(e),
            details={"cmd": cmd},
        )
    except FileNotFoundError as e:
        return VerificationResult(
            status="abc_not_found",
            time_sec=time.time() - t0,
            raw_output=str(e),
            details={"cmd": cmd},
        )