# GrantShift Decision Log

## D-001 — Separate preference from authorization
**Decision.** Treat inferred preference and permission to act as distinct state variables.
**Alternatives.** Single intervention score; preference-as-permission heuristic.
**Evidence.** Factorial and evidence-channel ablations.
**Trade-off.** More state/evaluation complexity, but clearer failure attribution.
**Outcome.** Became the core experimental axis.

## D-002 — Prefer outcome/state graders over self-reported success
**Decision.** Grade mutated environment state and authorization ledger, not an agent's textual claim that a task is done.
**Alternatives.** Transcript-only LLM judge; exact trajectory matching.
**Evidence.** Multi-turn trajectory harness design.
**Trade-off.** More environment instrumentation, less susceptibility to plausible-but-false completion text.
**Outcome.** Four-grader trajectory stack plus verified state outcomes.

## D-003 — Use pass@k and pass^k
**Decision.** Report repeated-trial reliability, not only pass@1.
**Alternatives.** Single aggregate success rate.
**Evidence.** Noisy authorization-first policy: high pass@1 but materially lower pass^5.
**Trade-off.** More trials/compute; exposes customer-facing reliability risk.
**Outcome.** Repeated-trial metrics retained.

## D-004 — Do not headline canonical classifier accuracy
**Decision.** Treat canonical accuracy as a mechanism check, not the project result.
**Alternatives.** Lead with ~99% exact.
**Evidence.** Paraphrase collapse to ~52.8%.
**Trade-off.** Less impressive superficial number, much more defensible story.
**Outcome.** Robustness failure became a first-class result.

## D-005 — Move from labels to scoped capabilities
**Decision.** Model authorization as a scoped, time-varying capability.
**Alternatives.** Latest authorization label; flat boolean permission.
**Evidence.** Scope-bound and provenance challenges.
**Trade-off.** More complex state machine and benchmark semantics.
**Outcome.** Latest-label shortcut becomes falsifiable.

## D-006 — Add lifecycle/provenance rather than more synthetic volume
**Decision.** Increase semantic difficulty instead of simply generating more IID cases.
**Alternatives.** Larger lexical dataset.
**Evidence.** Latest-label and flat-provenance failures under replay, expiry, delegation and concurrent requests.
**Trade-off.** Smaller but more diagnostic challenge families.
**Outcome.** Capability ledger challenge.

## D-007 — Mutation-test the benchmark itself
**Decision.** Release only if intentionally broken invariants are detected.
**Alternatives.** Validate only the reference implementation.
**Evidence.** Initial mutation suite exposed five benchmark blind spots.
**Trade-off.** More work and less flattering intermediate result.
**Outcome.** Expanded isolation families and mutation-complete release gate.

## D-008 — Stop synthetic escalation at the evidence boundary
**Decision.** The next major claim requires real frontier/human/external-environment evidence rather than another synthetic benchmark layer.
**Alternatives.** Continue adding synthetic challenge families and market them as SOTA.
**Evidence.** Evidence hierarchy and novelty audit.
**Trade-off.** Leaves an explicit unfinished empirical step.
**Outcome.** External runbook and frontier harness exist; no fabricated result is reported.
