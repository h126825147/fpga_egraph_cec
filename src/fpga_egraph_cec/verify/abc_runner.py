@dataclass
class VerificationResult:
    status: str
    time_sec: float
    raw_output: str
    details: dict

def run_abc_verify(aig_path: str, timeout_sec: int = 300) -> VerificationResult:
    ...