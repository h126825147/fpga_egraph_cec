from ..bench.loader import BenchmarkCase
from ..parser.aiger_parser import load_aag
from ..egg.normalize import normalize_circuit
from ..align.aligner import align_circuits
from ..miters.build import build_miter, build_aligned_miter
from ..verify.abc_runner import run_abc_verify


def run_experiment(cases: list[BenchmarkCase], config: dict) -> None:
    for case in cases:
        circuit = load_aag(case.path)
        norm = normalize_circuit(circuit)
        aligned = align_circuits(norm, norm)
        standard_miter = build_miter(norm, norm)
        aligned_miter = build_aligned_miter(norm, norm, aligned)
        # export and verify should be added here
        print(case.name, norm.size(), aligned.score, standard_miter.size(), aligned_miter.size())