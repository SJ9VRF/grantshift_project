# Empirical status

## Completed and executable
- 6,000-case natural-language factorial synthetic pilot.
- Base-grouped train/dev/test splits; no counterfactual siblings cross splits.
- Blinded inputs separated from gold/latent factors.
- C0-C3 information ablations (state / preference / authorization / full).
- Always-ask, always-silent, always-act, always-suggest baselines.
- Burden, unauthorized-action, unnecessary-intervention, missed-opportunity, and synthetic-utility metrics.
- 100-turn drift simulator and stylized consequence environment.
- Human-study protocol and power-analysis tool.
- Frontier-model prompt export and provider-neutral scoring harness.
- Croissant metadata.

## Not completed and not claimed
- IRB/ethics-approved participant data collection.
- Human gold labels or inter-annotator agreement.
- External frontier-model runs.
- Real-tool or Android/SWE/browser benchmark audit.
- Prospective longitudinal user deployment.

These are empirical dependencies, not software TODOs. Fabricating them would invalidate the paper.

## Version 1.2.0 robustness

Executed synthetic evidence now includes evidence-channel shuffles/masks, five train-base subsample fits, leave-one-domain-out evaluation, and a train-only surface-augmentation mitigation. These strengthen internal validity of the mechanism pilot but do not substitute for human judgments, frontier-model outputs, or external interactive tasks.

## Version 1.2.0 trajectory mechanics

Executed locally:

- 144 stateful tasks across six domains;
- 2,880 trials (5 trials per task/policy across four policy adapters);
- full trajectories and final-state outcomes;
- deterministic authorization/outcome/efficiency/recovery graders;
- pass@k and pass^k reliability summaries;
- 1,142 mined incidents and 1,142 failure-derived training records.

Not executed or claimed:

- real browser/GUI/computer-use environments;
- frontier-model agent trajectories;
- human-calibrated model graders;
- frontier-model SFT/DPO/RL runs using the exported training records;
- production A/B tests.

## GrantShift v1.2.0 dynamic-authorization study

Executed locally:

- 1,260 controlled authorization-transition trajectories across six domains, three fixed preference histories, seven transition families, and ten lexical replicates;
- transition families: grant, revoke, expire, supersede, delayed confirmation, deny-after-ask, and stale confirmation after material task change;
- preference evidence is held fixed within a trajectory while task-specific authority changes;
- metrics include exact transition response, stale-authority execution, premature execution, repeated asks, and authorization-update latency;
- static-initial-authority baseline: 47.1% exact and 11.8% stale-authority execution;
- preference-first baseline: 35.3% exact and 13.7% premature execution;
- latest-authority and explicit authorization-state-machine mechanism policies: 100% exact with 0% stale/premature execution in this deterministic synthetic suite.

These numbers validate the benchmark mechanics. They are **not** frontier-model, human-normative, deployment-safety, or SOTA claims.

## Added in v1.2

Completed locally:
- 1,080 scope-bound adversarial authorization trajectories;
- 3,240 evaluated steps across preference-first, latest-label, and scope-aware policies;
- trajectory-cluster bootstrap confidence intervals;
- paired exact comparison;
- provider-neutral export/scoring of 6,300 transition prompts.

Still not completed: actual frontier-model predictions on those prompts or external-environment ports.
