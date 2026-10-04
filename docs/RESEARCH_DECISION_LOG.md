# Research decision log

This log records decisions that materially changed the research claim. It is intentionally short and falsifiable.

## D1 — Separate preference from permission
The first prototype treated a user preference for autonomy as evidence that the agent could act. Counterfactual authorization tests exposed this as an overreach failure. The project therefore treats preference and authorization as distinct variables.

## D2 — Stop using oracle-visible scalar inputs
Early structured pilots exposed the same latent factors used by the synthetic oracle. Those runs are retained as mechanism checks, but the main factorial suite uses natural-language history/situations and grouped base-scenario splits.

## D3 — Do not headline canonical accuracy
Held-out paraphrases caused a large accuracy drop. Canonical accuracy is therefore reported with the paraphrase stress test and surface-augmentation result.

## D4 — Evaluate trajectories, not only decisions
A correct first action can still lead to a bad outcome. The agent-eval harness grades authorization, outcome state, interaction efficiency, and recovery over repeated trials.

## D5 — Track authorization state over time
Delayed confirmation and permission revocation break static policies. The cross-environment suite therefore evaluates state-tracking policies under changing authorization and tool failures.

## D6 — Keep external evidence separate
No human-participant, frontier-model, or external production-benchmark result is reported until the corresponding run exists. Harnesses are provided, but readiness is not evidence.

## D7 — Narrow the novelty claim to authorization transitions
A September 2026 literature audit found substantial prior work on proactive personalization, consent, overreach, long-horizon user context, and revocation. The broad claim “personalized agents need permission awareness” is therefore not treated as novel. GrantShift narrows the controlled contribution to holding preference evidence fixed while task-specific authorization transitions through grant, delay, denial, revocation, expiration, supersession, and stale-confirmation invalidation.
