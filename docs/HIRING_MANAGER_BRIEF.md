# GrantShift - one-page research brief

**Aura Yavary**

## The problem
Personalized agents learn what a user tends to want, but a remembered preference is not a standing authorization. Real authority changes: users confirm, revoke, narrow, expire, or materially change an action after confirming it. A capable agent can therefore be personalized and still act under stale permission.

## The research move
GrantShift treats authorization as a **time-varying, scope-bound state** rather than a static label. The benchmark holds preference evidence fixed while changing authority, making it possible to isolate stale-permission behavior from ordinary personalization error.

## What is implemented
- 1,260 matched authorization-transition trajectories across 6 domains and 7 transition families.
- 1,080 adversarial scope/version trajectories where old grants must not transfer to changed actions.
- 6,000 preference-by-authorization counterfactual decisions + 900 paraphrase stress cases.
- Multi-turn executable environment, verified end-state graders, repeated trials, pass@k/pass^k, environment shifts, incident mining, and post-training record export.
- Provider-neutral frontier-model prompt/export/scoring harness and human-study protocol.
- Claim-to-evidence gating, novelty audit, reproducible release, anonymous paper bundle, and CI tests.

## Most diagnostic result
A policy that reads the **latest authorization label** scores 100% on the simple transition suite but only **88.9%** on scope-bound adversarial transitions, with **11.1% stale-scope execution**. A scope-aware state machine reaches 100% in the deterministic synthetic instrument. The point is not that a hand-written state machine is SOTA; it is that the adversarial suite reveals a failure hidden by the easier benchmark.

## What the project does *not* claim
No human-validity, production-safety, or frontier-model SOTA claim is made without the corresponding experiment. The next decisive study is to run the same matched transition interventions on contemporary frontier agents and at least one external realistic environment.

## Why this is relevant to frontier-agent work
The project is an end-to-end loop: ambiguous behavioral problem -> formal variable separation -> benchmark -> adversarial stress test -> trajectory/environment grader -> failure taxonomy -> training-data export -> reproducible claim audit. That is the same research-engineering shape required to turn messy model behavior into measurable hypotheses and post-training signal.

## Authorization provenance: the strongest falsification test

GrantShift v1.2 goes beyond scope/version tracking. Grants are bound to principal, request, resource, revision, and nonce. A policy that simply maps the latest `granted` label to ACT falls to 66.7% exact and 33.3% invalid-provenance execution across replay, wrong-principal, cross-request, revision-change, and delegation-revocation cases. This is a stronger signal than a high synthetic benchmark score because it documents a shortcut, constructs a targeted adversarial test, and demonstrates what state representation the harness must preserve.
