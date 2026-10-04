# Model Card — GrantShift Intervention Policies

The repository includes heuristic, generic learned, personalized learned, calibrated-wrapper, and pairwise reward baselines. They are small local research models, not deployment-ready personal assistants.

Key safety-sensitive outputs are `ACT` and interventions on high-stakes/financial/privacy-sensitive states. The benchmark tracks autonomy violations explicitly. Real deployment would require stronger permissioning, tool-specific confirmation policies, human evaluation, privacy review, and external red-team testing.

## Authorization-first release policy

GrantShift includes an auditable wrapper with precedence `authorization > recoverability > personalization`. Explicit prohibition forces non-intervention; confirmation-required states downgrade stronger actions to asking; low-recoverability autonomous execution is downgraded to asking. This is intentionally not presented as a complete safety solution.

The matched frontier set shows why the constraint matters in this synthetic setting: the unconstrained personalized policy reaches 50.4% exact with 80.6% false-proactivity, while the personalized authorization-first policy reaches 87.9% exact with 0% false-proactivity. A generic policy with the same authorization gate reaches 89.6% exact / 99.2% acceptable, so permission structure—not personalization—is the dominant factor on this authorization-shift stress test. A stricter constrained ranker lowers mean overreach to 0.025 while reducing exact accuracy, exposing an accuracy–restraint tradeoff.

**Author:** Aura Yavary

## v1.3 trajectory evaluation boundary

GrantShift now includes a local stateful agent sandbox and repeated-trial reliability evaluation. The deterministic authorization-first adapter reaches saturation in this controlled environment by design; this is a regression/infrastructure result, not evidence that a frontier agent is solved. The 8% seeded-noise adapter is included to make consistency metrics observable. Real tool execution, model-based graders, and frontier-model post-training remain outside the executed evidence in this release.

## v1.2 scope-bound authorization boundary

A free-floating `granted` label is not sufficient when the underlying action changes. v1.2 adds a synthetic adversarial suite in which grants are explicitly bound to task scope/version. The latest-label baseline reaches 88.9% exact and 11.1% stale-scope execution, while a scope-aware state machine is exact in the deterministic instrument. These numbers test the benchmark mechanism; they are not model-safety or deployment claims.

For high-consequence actions, deterministic capability and authorization enforcement remains desirable outside the model. GrantShift targets the behavioral/harness layer: whether an agent requests, waits, interprets, and updates authority correctly before an external enforcement boundary is reached.

## v1.2 authorization provenance boundary

A grant is treated as valid only when its principal, request ID, resource, and revision match the current operation and the authority chain has not been revoked. The 864-trajectory provenance challenge includes replay, cross-request confusion, wrong-principal confirmation, resource/revision changes, and delegated-authority revocation. The deterministic latest-label baseline reaches 66.7% exact with 33.3% invalid-provenance execution; the explicit provenance state machine reaches 100% exact. These are instrument checks, not frontier-model results.

## Capability-ledger limitation

The capability ledger is a deterministic reference policy used to validate the evaluation instrument. Its 100% synthetic score must not be interpreted as a learned-model result, a universal normative authorization policy, or deployment safety evidence.

## Mutation sensitivity
The v1.4 release intentionally deletes individual capability-validity checks. Every targeted mutant is detected by the final challenge; a zero-drop mutant fails the release gate. This validates benchmark coverage, not real-model safety.
