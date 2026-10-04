# Compute and runtime disclosure

The bundled synthetic v2 mechanism-check pipeline was measured on the release container, not on accelerator hardware.

- Platform: Linux x86_64
- CPU allocation visible to the process: 5 logical CPUs
- Python: 3.13.5
- NumPy: 2.3.5
- pandas: 2.2.3
- scikit-learn: 1.8.0
- GPU/TPU: none used for the v2 classical baselines
- Measured peak resident memory for the v2 generation/evaluation block: 206,320 KB
- Measured elapsed time for generation + C0-C3 factorial evaluation + paraphrase stress test + 100-turn drift simulation: 6.71 seconds

The full legacy release pipeline contains additional diagnostic experiments and can take materially longer. The publication-facing v2 results do not require GPU compute.

External frontier-model evaluation is intentionally not included in this disclosure because no external model API/weights were executed in this archive. Human-study compute is likewise not applicable until data collection occurs.

## v1.3 trajectory suite

The trajectory harness is CPU-only and executes 2,880 local sandbox trials. It does not call an external model API. Runtime and peak memory were measured on the release container with `/usr/bin/time -v`: **0.88 s wall-clock** and **144,792 KB peak RSS** for the 2,880-trial trajectory run. The sandbox policy latency is microsecond-scale because the included adapters are deterministic Python baselines, not neural agents, and should not be compared with frontier-model latency.
