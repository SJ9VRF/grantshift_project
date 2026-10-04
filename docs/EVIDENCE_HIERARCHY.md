# GrantShift Evidence Hierarchy

GrantShift separates what is **implemented**, what is **measured in synthetic instruments**, and what still requires **external empirical evidence**.

## Level 0 - Specification
Machine-readable authorization semantics, capability invariants, action schema, and claim registry.

## Level 1 - Deterministic mechanism tests
Matched preference/authorization counterfactuals, transition suites, scope/provenance/capability-ledger challenges, and environment-state verification. These validate whether the evaluation can distinguish known failure modes. They are not evidence about frontier-model prevalence.

## Level 2 - Falsification and mutation sensitivity
Simpler policies and deliberately broken ledgers are expected to fail. The release gate requires every targeted invariant mutant to be detected. In v1.4, mutation analysis exposed blind spots for nonce, request, principal, resource, and revision validity; dedicated isolation families were added before release.

## Level 3 - Repeated stochastic sandbox trials
Seeded action noise, pass@k/pass^k, long-horizon drift, state-shift recovery, and incident mining measure reliability under controlled stochasticity. Still synthetic.

## Level 4 - External model evaluation (prepared, not executed here)
Provider-neutral prompts, schemas, deduplicated prompt pools, scoring, power analysis, and result ledger. Claims about GPT/Claude behavior require actually running these adapters.

## Level 5 - Human validation (prepared, not executed here)
Preregistered matched judgments, acceptable-action sets, perceived control/helpfulness/annoyance, disagreement, and mixed-effects analysis.

## Level 6 - Production evidence
Real tool-use environments, deployment incidents, policy review, monitoring, and post-training impact. No production-safety claim is made in this release.

**Rule:** a public claim may only reference evidence at or below the level actually executed. Infrastructure for a higher level is not treated as evidence from that level.
