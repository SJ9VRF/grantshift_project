# GrantShift Experiment Journal

This journal is reconstructed from the executable artifacts that survived the GrantShift development process. It is not a fabricated historical lab notebook. Entries describe experiments that can be traced to scripts/results in this repository; where exact wall-clock chronology was not preserved, the journal uses research dependency order rather than invented dates.

## Exp-001 — Structured-factor baseline exposed a leakage problem
**Hypothesis.** A compact classifier could test whether preference and authorization are separable.
**Setup.** Early factorial evaluation with structured synthetic factors.
**Result.** High canonical accuracy was easy to obtain, but the setup exposed too much of the oracle-generating structure.
**Interpretation.** The result was not strong evidence about natural-language agents; it mostly validated the synthetic rule.
**Next decision.** Remove latent structured factors from evaluated input and separate public input from gold metadata.
**Evidence.** `experiments/run_v2_factorial.py`, `artifacts/v2_factorial_results.json`.

## Exp-002 — Natural-language factorial benchmark
**Hypothesis.** Preference and authorization can be manipulated independently while keeping counterfactual siblings grouped.
**Setup.** 6,000 natural-language cases; grouped train/dev/test split; preference × authorization factorial design.
**Result.** Permission-aware conditions substantially outperformed state/preference-only conditions on the synthetic mechanism check.
**Interpretation.** Authorization evidence carries information not recoverable from preference alone.
**Next decision.** Stress-test surface-form generalization rather than headline canonical accuracy.
**Evidence.** `silensiabench/v2/`, `artifacts/v2_factorial_results.json`.

## Exp-003 — Held-out paraphrase collapse
**Hypothesis.** Canonical performance would transfer to unseen phrasing.
**Setup.** 900 held-out paraphrase cases.
**Result.** Canonical-only baseline fell from about 98.7% exact to 52.8% exact and became excessively question-heavy.
**Interpretation.** The model had learned substantial surface/template shortcuts.
**Next decision.** Treat this as a negative result; add train-only surface augmentation and explicit robustness tests.
**Evidence.** `experiments/run_v2_surface_generalization.py`, `artifacts/v2_surface_generalization.json`.

## Exp-004 — Surface augmentation repaired the shortcut
**Hypothesis.** Adding a second training surface only for training bases would improve paraphrase transfer without leaking test siblings.
**Setup.** Train-only surface augmentation.
**Result.** Paraphrase exact recovered to roughly 99.0% while canonical remained roughly 99.1%.
**Interpretation.** The earlier failure was largely surface coverage, not evidence that the formulation itself was impossible.
**Next decision.** Add negative controls that shuffle/mask evidence channels.
**Evidence.** `artifacts/v2_robustness_suite.json`.

## Exp-005 — Evidence-channel negative controls
**Hypothesis.** Authorization evidence, rather than domain/template cues, is the dominant signal for safe action.
**Setup.** Shuffle/mask authorization; shuffle preference.
**Result.** Authorization ablations caused a much larger collapse than preference shuffling and reintroduced unauthorized actions.
**Interpretation.** Preference and authorization are behaviorally distinct channels in the instrument.
**Next decision.** Move from one-step classification to trajectory/state evaluation.
**Evidence.** `experiments/run_v2_robustness_suite.py`, `artifacts/v2_robustness_suite.json`.

## Exp-006 — Multi-turn trajectory harness
**Hypothesis.** Decision accuracy hides repeated-run and recovery failures.
**Setup.** 144 tasks, multiple trials, state-based outcome grading, authorization/outcome/efficiency/recovery graders.
**Result.** Noisy authorization-first policy retained high pass@1 but lower pass^5, exposing reliability loss across repeated executions.
**Interpretation.** Single-run averages were insufficient.
**Next decision.** Add changing-world authorization events.
**Evidence.** `experiments/run_agent_trajectory_eval.py`, `artifacts/trajectory_eval.json`.

## Exp-007 — Delayed confirmation broke the static policy
**Hypothesis.** Knowing the authorization rule is sufficient under state changes.
**Setup.** Delayed confirmation, revocation, transient tool failure.
**Result.** Static authorization-first repeatedly asked during delayed confirmation instead of tracking pending state.
**Interpretation.** Rule knowledge and state tracking are different capabilities.
**Next decision.** Introduce explicit state-tracking policy.
**Evidence.** `experiments/run_cross_environment_eval.py`, `artifacts/cross_environment_eval.json`.

## Exp-008 — Latest-label shortcut looked perfect
**Hypothesis.** Tracking the latest authorization label may be enough.
**Setup.** Controlled authorization transitions.
**Result.** Latest-label and state-machine policies could both appear perfect on the easier transition suite.
**Interpretation.** The benchmark itself was too weak to justify the stronger state-machine claim.
**Next decision.** Bind grants to action scope/version and construct adversarial stale-scope cases.
**Evidence.** `experiments/run_authorization_transition_eval.py`, `artifacts/authorization_transition_eval.json`.

## Exp-009 — Scope-bound authorization falsified latest-label tracking
**Hypothesis.** A grant for one action version should not transfer to a materially changed action.
**Setup.** Scope/version changes and stale confirmations.
**Result.** Latest-label exact fell to 88.9% with 11.1% stale-scope execution; scope-aware tracking remained exact on the deterministic instrument.
**Interpretation.** Authorization is not merely a time-varying label; it is scoped.
**Next decision.** Add provenance dimensions beyond scope/version.
**Evidence.** `experiments/run_scope_bound_authorization_eval.py`, `artifacts/scope_bound_authorization_eval.json`.

## Exp-010 — Provenance challenge
**Hypothesis.** Authorization must bind principal, request, resource/action, revision, and nonce.
**Setup.** Wrong-principal confirmation, replay, concurrent-request cross-wire, resource/revision changes, delegated-authority revocation.
**Result.** Latest-label policy fell to 66.7% exact with 33.3% invalid-provenance execution; provenance-aware tracking remained exact on the deterministic instrument.
**Interpretation.** Flat authorization state loses causal provenance.
**Next decision.** Test composition: expiry, revocation ancestry, replay history, and delegation.
**Evidence.** `experiments/run_authorization_provenance_eval.py`, `artifacts/authorization_provenance_eval.json`.

## Exp-011 — Capability ledger and a bug in our own policy
**Hypothesis.** Provenance plus lifecycle state is needed for composed authority changes.
**Setup.** Expiry, parent delegation, concurrent confirmation reorder, principal switch, replay.
**Result.** Flat provenance remained vulnerable. The first ledger implementation also failed because a revoked delegated token fell through to an overly permissive ASK path.
**Interpretation.** The benchmark falsified our own implementation, not just baselines.
**Next decision.** Refine the invariant: replay of revoked authority must not silently reopen authorization; distinguish same-principal replay from a genuinely changed active principal.
**Evidence.** `experiments/run_capability_ledger_eval.py`, `artifacts/capability_ledger_eval.json`, `configs/authorization_state_machine.json`.

## Exp-012 — Mutation testing falsified the benchmark
**Hypothesis.** Every claimed ledger invariant is independently exercised by the benchmark.
**Setup.** Remove expiry, nonce revocation, parent revocation, request/principal/resource/revision binding one at a time.
**Result.** Initial mutation analysis found five blind spots: several broken invariants still scored 100%.
**Interpretation.** Passing the reference policy did not prove benchmark coverage.
**Next decision.** Add direct isolation families for each blind invariant and rerun the mutation gate.
**Evidence.** `experiments/run_capability_mutation_eval.py`, `artifacts/capability_mutation_eval.json`.

## Exp-013 — Mutation-complete capability challenge
**Hypothesis.** Each targeted invariant should produce a measurable failure when removed.
**Setup.** Expanded 1,440-trajectory / 5,760-step capability challenge with direct nonce, request, principal, resource, and revision isolation families.
**Result.** All targeted mutants are detected; full ledger 100%/0% invalid execution, while each broken invariant produces a measurable regression on the deterministic instrument.
**Interpretation.** The evaluation now tests its own claimed coverage rather than only the reference implementation.
**Next decision.** Stop adding synthetic sophistication and move the next evidence level to frontier-model and human/external-environment runs.
**Evidence.** `artifacts/capability_mutation_eval.json`, `artifacts/capability_ledger_eval.json`.
