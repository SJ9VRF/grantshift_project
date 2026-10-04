# GrantShift Engineering Report

**Author:** Aura Yavary

## System objective
GrantShift separates user preference from permission. The decision layer chooses among seven intervention modes—act, ask, suggest, remind, wait, defer, or do nothing—while an explicit authorization/recoverability envelope constrains what the policy may do.

## Core architecture
1. Structured `AgentState` captures urgency, intent/execution confidence, stakes, reversibility, expected benefit, financial/social/privacy/safety risk, time sensitivity, and user profile.
2. A learned intervention policy estimates action probabilities.
3. An authorization layer interprets `advisory`, `ask_required`, `preauthorized`, and `prohibited` states plus recoverability.
4. Authorization-first and constrained-ranking variants enforce the permission envelope.
5. Evaluation measures exact action choice, acceptable-action rate, false proactivity, missed opportunities, authorization ceiling violations, minimal sufficient action, overreach distance, calibration, counterfactual consistency, and OOD behavior.

## Training and calibration
The research baseline uses a scikit-learn preprocessing pipeline plus class-balanced logistic regression. Numeric features are imputed and standardized, categorical features are one-hot encoded, and the goal text is represented with TF-IDF n-grams. Temperature scaling is fit only on a held-out development split.

## Benchmark methodology
GrantShiftBench includes 600 main scenarios, 160 matched preference counterfactuals, and 240 matched authorization counterfactuals (60 base situations × four authorization states). The matched sets are designed to isolate one causal variable at a time rather than reward broad scenario memorization.

## Failure-driven development
The strongest failure found during development was that unconstrained personalization could amplify overreach on permission counterfactuals. This motivated explicit authorization-first and constrained-ranking policies. The repo keeps both stronger and weaker baselines rather than hiding the tradeoff.

## Reproducibility
`make all` regenerates benchmark data, trains/exports the policy, runs IID/OOD/counterfactual evaluations, drift simulation, calibration, ablations, diagnostics, tests, and release audits. The wheel and CLI are smoke-tested from a clean target directory.

## Current boundary
This release is a controlled decision-layer research artifact, not a production autonomous agent. It does not execute external tools, spend money, send messages, or perform irreversible actions. Real tool execution should be added only behind explicit confirmation, verification, idempotency, and human-escalation controls.

## v1.3 trajectory evaluation

The decision policy is now embedded in a small stateful environment. The evaluation harness records task, trial, trajectory, grader outputs, and final outcome separately. This matters because a model's statement that an action succeeded is not accepted as evidence of success; the environment state is the source of truth.

The executed suite has 144 tasks across six domains, four grader dimensions, and five repeated trials per policy/task. A seeded-noise policy is included to test repeated-run reliability. Failed trajectories are mined into a typed incident bank and exported as weighted preference-training records.

This environment is deliberately narrower than WebArena/OSWorld-style evaluation. It validates evaluation machinery and behavioral invariants locally; it does not establish performance in production software.
