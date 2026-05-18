1. 重新预处理 benchmark
bash
python scripts/prepare_benchmarks.py --benchmarks data/raw/benchmarks/benchmarks.yaml

2. 跑 smoke
bash
python scripts/run_batch.py --config configs/exp_default.yaml --group smoke --benchmarks data/raw/benchmarks/benchmarks.prepared.yaml

3. 再跑 all
bash
python scripts/run_batch.py --config configs/exp_default.yaml --group all --benchmarks data/raw/benchmarks/benchmarks.prepared.yaml
