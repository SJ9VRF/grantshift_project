# Skeptical Reviewer Red-Team

This document tries to weaken GrantShift's own story rather than sell it.

## Attack 1 — "The 100% result is engineered into the oracle"
**Valid concern.** The capability-ledger result is deterministic synthetic mechanism validation. It does not establish model competence or deployment safety.

**What survives.** Mutation analysis is still useful because intentionally deleting each invariant causes measurable failure; the benchmark can detect the specific mechanism it claims to test.

**What does not survive.** Any claim that a frontier model will implement the ledger correctly.

## Attack 2 — "The benchmark was adapted until the reference method won"
**Valid concern.** Benchmark evolution followed discovered failures.

**Counter-evidence.** Mutation testing initially rejected the benchmark itself: several broken invariants scored 100%. Those blind spots were retained in the experiment journal and the benchmark was expanded before the release gate was allowed to pass.

**Remaining risk.** The final families may still omit unanticipated real-world ambiguity.

## Attack 3 — "Authorization semantics are hand-written"
**Valid concern.** Yes. Current gold labels encode controlled semantics, not human consensus.

**Required next evidence.** Human labels on ambiguous cases, inter-annotator agreement, and explicit disagreement analysis.

## Attack 4 — "A deterministic guardrail could solve this without an LLM"
**Mostly true for irreversible actions.** GrantShift should not be interpreted as an argument against deterministic enforcement. It studies whether the behavioral/evaluation layer preserves authority state before the enforcement boundary.

## Attack 5 — "Synthetic sophistication can become benchmark theater"
**Valid concern.** The project therefore stops treating additional synthetic complexity as the next evidence level. The next material result should come from external frontier models, multiple harnesses, human judgments, or a realistic tool environment.

## Reviewer verdict boundary
The current package supports: a well-specified evaluation mechanism, falsification history, mutation-sensitive coverage, reproducible synthetic results, and a failure-to-training-data research interface.

It does **not** support: SOTA claims, human-validity claims, production-safety claims, or model-improvement claims.
