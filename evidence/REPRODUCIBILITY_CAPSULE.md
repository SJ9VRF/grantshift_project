# Reproducibility Capsule

## Fast path

```bash
python scripts/reproduce_core_evidence.py
```

This reruns the two core capability experiments, rebuilds the claim→experiment→artifact evidence graph, validates the claim registry, checks public-number consistency, and writes `artifacts/core_reproduction_report.json` with command outcomes and SHA-256 hashes.

## Full test suite

```bash
PYTHONPATH=. pytest -q
```

## Scope
The fast path deliberately does not pretend to reproduce external model or human results: none are claimed in this release. It reproduces the synthetic mechanism evidence that underlies the homepage and research narrative.
