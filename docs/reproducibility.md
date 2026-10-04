# Reproducibility

Python 3.11+ is recommended. The project intentionally uses lightweight local models so the full benchmark, training and evaluation loop can run without paid APIs or proprietary checkpoints.

```bash
pip install -e .
python grantshiftbench/generators/generate_v1.py
python experiments/run_full_eval.py
python experiments/run_ablations.py
python experiments/run_preference_reward.py
python experiments/run_drift_simulation.py
python dashboard/build_dashboard.py
pytest -q
```

All generated scenarios use a fixed seed and fixed train/dev/test split. Results are written to `artifacts/`.
