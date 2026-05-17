from __future__ import annotations

from dataclasses import dataclass
import subprocess
import time


@dataclass
class VerificationResult:
    status: str
    time_sec: float
    raw_output: str
    details: dict


def run_abc_verify(aig_path: str, timeout_sec: int = 300, abc_bin: str = "abc") -> VerificationResult:
    t0 = time.time()
    try:
        cmd = [abc_bin, "-c", f"read {aig_path}; strash; cec"]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_sec)
        out = proc.stdout + "\n" + proc.stderr

        status = "unknown"
        if "Networks are equivalent" in out or "equivalent" in out.lower():
            status = "equivalent"
        elif "Networks are NOT equivalent" in out or "not equivalent" in out.lower():
            status = "not_equivalent"

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