# Experiment registry

| Experiment | Question | Primary metric | Artifact |
|---|---|---|---|
| Factorial v2 | Does preference differ from permission evidence? | exact / unauthorized act / burden | `artifacts/v2_factorial_results.json` |
| Surface generalization | Is the policy robust to unseen phrasing? | exact / burden | `artifacts/v2_surface_generalization.json` |
| Evidence controls | Which evidence channel drives behavior? | delta exact / unauthorized act | `artifacts/v2_robustness_suite.json` |
| Long horizon | How quickly does behavior adapt after preference drift? | adaptation latency / regret | `artifacts/long_horizon_v2.json` |
| Trajectory eval | Does a decision lead to the correct verified outcome? | pass@1 / pass^k / grader passes | `artifacts/trajectory_eval.json` |
| Environment shift | Does policy track confirmation/revocation/tool state? | pass@1 / pass^5 | `artifacts/cross_environment_eval.json` |
| Authorization transitions | What breaks when preference stays fixed but task authority changes? | stale-authority execution / premature execution / repeated asks / update latency | `artifacts/authorization_transition_eval.json` |
| Grader regression | Are edge-case rubric decisions stable? | case pass rate | `artifacts/grader_rubric_regression.json` |
| Failure flywheel | Can failures become prioritized training records? | incident coverage | `artifacts/incident_bank.json` |

External experiments are deliberately not listed as completed: human validation, frontier-model evaluation, and external interactive benchmark evaluation remain pending execution.

## E8 - Scope-bound authorization adversarial test
- **Question:** Is reading the latest authorization label sufficient when a grant is bound to a specific action version?
- **Dataset:** `grantshiftbench/adversarial/scope_bound_transitions.jsonl` (1,080 trajectories / 3,240 steps).
- **Primary metrics:** exact action, stale-scope execution, premature execution.
- **Negative control:** latest-authorization-label policy.
- **Mitigation:** scope-bound state machine tracking grant provenance.
- **Artifacts:** `artifacts/scope_bound_authorization_eval.json`, `artifacts/scope_bound_authorization_trials.jsonl`, `artifacts/transition_statistics.json`.
- **Status:** completed synthetic mechanism test; external frontier-model validation pending.
