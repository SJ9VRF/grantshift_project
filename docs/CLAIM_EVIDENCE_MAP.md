# Claim → evidence map

GrantShift deliberately separates **what the executed release establishes** from **what still needs human or frontier-model validation**. Every public research claim is tied to a machine-readable artifact in `configs/claim_evidence_registry.json`.

| Claim | Executed evidence | Scope |
|---|---|---|
| Preference and authorization are distinct signals in the controlled protocol | `v2_factorial_results.json`, `v2_robustness_suite.json` | synthetic mechanism |
| Authorization evidence is causally important for preventing overreach in the baseline | `v2_robustness_suite.json` | synthetic mechanism |
| Canonical wording overstates generalization | `v2_surface_generalization.json` | synthetic mechanism |
| Single-trial pass rate can hide repeated-trial unreliability | `trajectory_eval.json` | synthetic agent sandbox |
| State tracking matters under delayed confirmation / tool failure | `cross_environment_eval.json` | synthetic agent sandbox |
| Dynamic authorization transitions reveal stale-authority/update-latency failures under fixed preference evidence | `authorization_transition_eval.json` | synthetic transition mechanism |
| Failed trajectories can feed a deterministic data flywheel | incident bank + training pairs | research infrastructure |

The registry explicitly forbids unsupported claims of frontier-model SOTA, human preference validity, deployment safety, or successful production post-training.
