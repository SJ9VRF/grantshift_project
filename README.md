# GrantShift

## Stress-Testing Dynamic Authorization in Personalized AI Agents

**Aura Yavary**

GrantShift is a research/evaluation stack for a narrow failure mode in personal agents: **the user can keep wanting the same thing while the agent's authority to do it changes.** A personalized agent that correctly learned the user's preferences can still act on a stale grant, repeat a confirmation while a response is pending, execute after revocation, or reuse consent after the task materially changes.

The project deliberately separates two questions:

1. **Preference:** what does the user tend to want?
2. **Authorization:** what may the agent do *now*?

The scientific contribution is not “permission matters.” That is established. GrantShift's primary controlled factor is the **authorization transition**.

## Novelty status

A targeted literature/web audit through **25 September 2026** found substantial prior work on proactive personalized agents, consent handling, overreach, long-horizon changing environments, permission policies, and revocation. GrantShift therefore makes a narrower claim: we did not identify a released benchmark whose primary controlled design keeps preference evidence fixed while systematically transitions authorization across **grant, delayed confirmation, denial, revocation, expiration, supersession, and stale-confirmation invalidation**, with trajectory-level stale-authority/update-latency metrics.

See [`docs/NOVELTY_AUDIT.md`](docs/NOVELTY_AUDIT.md) for the closest-work matrix and explicit non-claims.

## GrantShiftBench: authorization transitions

The new core slice contains **1,260 controlled trajectories**:

- 6 domains × 3 fixed preference histories × 7 authorization-transition families × 10 lexical replicates;
- 3,060 labeled transition steps;
- matched preference evidence within each trajectory;
- separate metrics for stale execution, premature execution, repeated asking, and authority-update latency.

| Policy | Exact | Stale-authority execution | Premature execution | Update latency |
|---|---:|---:|---:|---:|
| Static initial authority | 47.1% | 11.8% | 0.0% | 0.89 steps |
| Preference first | 35.3% | 3.9% | 13.7% | 0.59 steps |
| Latest authorization state | 100% | 0.0% | 0.0% | 0.00 steps |
| Authorization state machine | **100%** | **0.0%** | **0.0%** | **0.00 steps** |

These are **synthetic mechanism checks**. They show that the benchmark distinguishes stale/static policies from state-tracking policies; they do not establish frontier-model SOTA.

## Scope-bound adversarial authorization

The base transition suite has a useful but important shortcut: a policy can score 100% by reading only the latest authorization label. GrantShift v1.2 adds **1,080 adversarial trajectories (3,240 steps)** where a grant is bound to a particular action scope/version and may become stale after a material task change or arrive late for an obsolete scope.

| Policy | Exact | Stale-scope execution |
|---|---:|---:|
| Preference first | 44.4% | 7.4% |
| Latest authorization label | 88.9% | **11.1%** |
| Scope-bound state machine | **100%** | **0.0%** |

Trajectory-cluster bootstrap 95% CI for the latest-label policy is **88.0-89.8% exact** and **10.2-12.0% stale-scope execution**. The paired exact comparison against the scope-aware state machine has 360 discordant steps, all in favor of scope tracking ($p<10^{-108}$). These statistics quantify a deterministic synthetic instrument, not model or human population performance.

The result fixes a real weakness in the simpler suite: **`granted` is not enough; the agent must know what action/version was granted.**

## Authorization provenance challenge

Scope/version binding is still incomplete if the agent ignores *who* granted authority, *which request* the grant belongs to, or whether a confirmation token is being replayed. GrantShift v1.2 adds an **864-trajectory / 2,592-step provenance challenge** in which each grant is bound to `principal + request_id + resource + revision + nonce`. The six adversarial families cover resource changes after grant, wrong-principal confirmation, nonce replay, concurrent-request cross-wiring, revision changes, and delegated-authority revocation.

| Policy | Exact | Invalid-provenance ACT |
|---|---:|---:|
| Preference first | 35.2% | 11.1% |
| Latest authorization label | **66.7%** | **33.3%** |
| Provenance-aware state machine | **100%** | **0.0%** |

The latest-label policy has a trajectory-cluster bootstrap exact rate of 66.7% (the deterministic construction makes the CI degenerate at 66.7%) and 864 paired discordant steps against the provenance-aware state machine, all favoring provenance tracking (`p < 10^-259`). Again, this is a synthetic falsification test, not a frontier-model leaderboard. The lesson is narrower and more useful: **authority is not only a state; it has provenance.**

For external model runs, the release exports 8,892 weighted prompt records but deduplicates them to **1,602 exact-unique prompts** to avoid wasting frontier-model budget on lexical replicates. An equivalence map expands predictions back to the weighted benchmark before scoring.

## Earlier controlled studies retained

GrantShift also retains the matched preference × authorization audit from the earlier prototype:

- 6,000 natural-language counterfactual cases;
- 900 unseen paraphrase cases;
- grouped counterfactual splits;
- burden, missed-opportunity and utility metrics;
- long-horizon preference drift;
- stateful trajectory evaluation and controlled environment shifts;
- incident mining and failure→training-pair export;
- human-study and frontier-model harnesses.

One deliberately negative result remains central: a full classical baseline reaches **98.7% exact** on the canonical synthetic set but falls to **52.8%** under unseen paraphrases. The project does not hide this shortcut sensitivity.

## Why this is not another generic “safe agent” demo

GrantShift tests a concrete causal asymmetry:

> **Preference can persist while authority changes.**

That is different from preference drift, generic context change, static task scope, and deterministic authorization enforcement. The benchmark asks whether the behavioral layer tracks the *latest valid grant* rather than the user's historical tendency or an earlier confirmation.

## Repository map

- `grantshiftbench/transitions/` — 1,260 authorization-transition trajectories and metadata
- `grantshiftbench/adversarial/` — 1,080 scope/version-bound authorization stress trajectories
- `grantshiftbench/provenance/` — 864 principal/request/resource/revision-bound provenance trajectories
- `experiments/run_authorization_transition_eval.py` — transition-policy evaluation
- `grantshiftbench/v2/` — 6,000 matched preference × authorization cases + 900 paraphrases
- `agent_eval/` — stateful task/trial/grader/trajectory harness
- `posttraining/` — failure mining, prioritization and chosen/rejected export
- `human_study/` — protocol, schema and power-analysis tooling
- `frontier_eval/` — blinded prompts and provider-neutral scorers, including 8,892 weighted transition/scope/provenance prompts and a 1,602-prompt exact-unique frontier pool
- `paper/` — public + anonymous paper source/PDF
- `docs/NOVELTY_AUDIT.md` — closest-work audit and defensible novelty claim
- `configs/claim_evidence_registry.json` — claim→artifact gating

## Reproduce the new core result

```bash
python grantshiftbench/transitions/generate.py
python experiments/run_authorization_transition_eval.py
python grantshiftbench/adversarial/generate.py
python experiments/run_scope_bound_authorization_eval.py
python grantshiftbench/provenance/generate.py
python experiments/run_authorization_provenance_eval.py
python experiments/run_provenance_statistics.py
python frontier_eval/deduplicate_prompts.py
python scripts/audit_benchmark_integrity.py
python experiments/run_transition_statistics.py
python frontier_eval/export_transition_prompts.py
pytest -q
```

## Evidence boundary

Completed locally:

- benchmark generation;
- synthetic transition mechanism tests;
- trajectory/state-shift tests;
- robustness and paraphrase stress tests;
- reproducibility/audit tooling.

**Not completed and not claimed:**

- human gold labels;
- frontier-model evaluation;
- external interactive-benchmark port;
- production deployment.

Those are the experiments required before claiming empirical SOTA.

## Citation

```bibtex
@misc{yavary2026grantshift,
  title  = {GrantShift: Stress-Testing Dynamic Authorization in Personalized AI Agents},
  author = {Aura Yavary},
  year   = {2026}
}
```

## v1.4 capability-ledger challenge

GrantShift v1.4 expands the compositional authorization challenge to 1,440 trajectories / 5,760 steps. Grants are treated as scoped capabilities whose validity depends on principal, request, resource, revision, nonce, expiry, revocation history, and delegation ancestry. A latest-label policy reaches 72.5% exact compliance with 27.5% invalid capability execution; flat provenance reaches 90.0% exact with 10.0% invalid execution; the explicit capability ledger reaches 100% exact with zero invalid execution in this deterministic synthetic mechanism test. A mutation suite then deletes seven invariants one at a time. Every mutant is detected: ignoring expiry falls to 95.0% exact / 5.0% invalid execution, while ignoring nonce, parent, request, principal, resource, or revision validity falls to 97.5% / 2.5%. The mutation gate originally exposed benchmark blind spots; the final challenge adds dedicated isolation families so no targeted mutant escapes. These are instrument-validation results, not frontier-model claims.

The public `project/trace_explorer.html` makes representative failure trajectories inspectable without reading JSON. The machine-readable state invariants are in `configs/authorization_state_machine.json`.

## Evidence layer
The polished project page is paired with an artifact-backed research record in `evidence/`. It includes the experiment journal, failed experiments, decision log, executed eval tables, unexpected findings, and an honest Git-history policy. Development history before v1.5.0 was not preserved and is not fabricated; incremental Git history begins from an explicitly labeled import snapshot and is exported as `artifacts/grantshift-history-v1.7.0.bundle`.

## Evidence integrity (v1.7)

GrantShift now ships a machine-readable evidence graph linking every registered research claim to experiment-journal entries and raw artifacts. `python scripts/reproduce_core_evidence.py` reruns the capability-ledger and mutation experiments, rebuilds the graph, validates claim evidence, and checks that public-facing numbers remain consistent. `evidence/REVIEWER_RED_TEAM.md` records the strongest skeptical interpretations and explicitly marks which conclusions do not follow from the synthetic results.
