# GrantShift novelty audit — 25 September 2026

## Verdict

**Broad idea: not novel. Narrow measurement contribution: defensibly novel, subject to external validation.**

It is no longer credible to claim novelty for any of the following by themselves: proactive personalized agents; act/ask/silence decisions; permission policies; agent overreach; long-horizon preference drift; changing-world personal-agent benchmarks; or authorization revocation. Strong 2026 work already covers each of these.

GrantShift is therefore scoped around a narrower question:

> **Can an agent keep a user's inferred preference fixed while correctly updating what it is allowed to do as authorization itself changes over time?**

The primary object is an **authorization transition**, not a static permission label. GrantShiftBench holds the task opportunity and preference history fixed while changing the authority state through grant, delayed confirmation, denial, revocation, expiration, supersession, and stale-confirmation invalidation. It measures whether behavior updates immediately rather than continuing under stale authority.

## Closest work and exact overlap

| Work | What it already establishes | What GrantShift must not claim | Remaining distinction |
|---|---|---|---|
| KnowU-Bench (2026) | Interactive mobile personalization; preference inference; consent seeking; act/ask/silence; post-rejection restraint | First personalized/proactive consent benchmark | Matched authorization-state transitions with preference held fixed are not its primary experimental factor |
| UserVille / PPP (2025) | Joint productivity, proactivity, personalization; interactive user simulation and training | First proactive-personalized training framework | GrantShift is an authorization-transition audit, not a general training environment |
| HorizonBench (2026) | Six-month histories and evolving preferences | First long-horizon preference-change benchmark | GrantShift changes **authority while preference stays fixed**, the complementary causal direction |
| ASTRA-bench (2026) | Tool use over time-evolving personal context | First context-aware personal tool benchmark | GrantShift isolates authorization transitions rather than general context complexity |
| VibeLifeBench (2026) | Multi-week living-world tasks, silent environment changes, act/ask/silence, implicit constraints | First persistent/changing-world life-agent benchmark | GrantShift focuses on authority validity and stale grants under controlled matched transitions |
| Yan (2026) | 113-person study of allow/ask/never policies and overreach | First evidence that permission policy design affects overreach | GrantShift is not a policy-interface user study; it tests dynamic authorization state tracking |
| OverEager-Bench / SNARE (2026) | Out-of-scope actions on benign coding tasks; large agent-model evaluations | First agent-overreach benchmark | GrantShift is personalized, domain-general, and targets **state changes in authorization**, not static task scope |
| Authorization Revocation (2026) | Formal root-scoped quiescence under delegation/asynchrony | First revocation formulation | GrantShift provides behavioral matched-counterfactual measurement across grant/revoke/expire/supersede/confirm transitions rather than a formal systems protocol |
| Bounded Agents / capability systems | Enforcement of bounded delegation and composition | First bounded-delegation mechanism | GrantShift evaluates the model/harness behavioral layer; it does not claim to replace deterministic enforcement |

## New primary benchmark slice

`GrantShiftBench Authorization Transitions` contains **1,260 controlled trajectories**:

- 6 everyday domains;
- 3 fixed preference histories;
- 7 authorization-transition families;
- 10 lexical replicates per cell.

Transition families:

1. grant;
2. revoke-before-execution;
3. expiration;
4. superseding instruction;
5. delayed confirmation;
6. deny-after-ask;
7. stale confirmation after material task change.

The preference history does **not** change inside a trajectory. This is deliberate. It makes the benchmark complementary to preference-drift work such as HorizonBench.

## Primary metrics

- **Stale-authority execution rate:** autonomous `ACT` after revoke, expiration, supersession, or denial.
- **Premature execution rate:** `ACT` while confirmation is still required.
- **Repeated-ask rate:** unnecessary repeated confirmation while a response is pending.
- **Authorization update latency:** number of steps until behavior reflects a changed authorization state.
- **Exact transition-policy compliance:** action matches the transition-specific oracle in the controlled synthetic mechanism test.

## Synthetic mechanism result

In the deterministic controlled benchmark:

- static-initial-authority baseline: **47.1% exact**, **11.8% stale-authority execution**, update latency **0.89 steps**;
- preference-first baseline: **35.3% exact**, with both stale and premature execution failures;
- explicit authorization-state-machine policy: **100% exact**, **0% stale-authority execution**, **0-step update latency**.

These numbers prove only that the benchmark distinguishes state-tracking policies from stale/static policies. They are **not frontier-model results** and are not a SOTA claim.

## Name audit

The prior name **Silensia** was replaced because the project needed a name tied to its actual scientific object rather than generic restraint. Several attractive alternatives were rejected because they already collide with current products/research, including `Pactra`, `Mandate`, `Delegent`, and `ScopeShift`.

A targeted web search on 25 September 2026 did not surface a directly matching AI-agent benchmark/research project called **GrantShift** or **GrantShiftBench**. This is a research-name collision check, not legal trademark clearance.

## Claim we are willing to make

> **To our knowledge, after a targeted search through 25 September 2026, we did not identify a released benchmark whose primary controlled factor holds personal preference evidence fixed while systematically transitioning task-specific authorization through grant, delayed confirmation, denial, revocation, expiration, supersession, and stale-confirmation invalidation, with trajectory-level stale-authority and update-latency metrics.**

This is deliberately narrower than “first permission benchmark,” “first proactive benchmark,” or “first revocation system.”

## What would be required for a strong SOTA claim

GrantShift is **not empirically SOTA yet**. A serious SOTA claim would require at minimum:

1. several contemporary frontier agents/models;
2. multiple real agent harnesses, because OverEager/SNARE show harness choice materially changes overreach;
3. human-validated authorization judgments and acceptable-action sets;
4. porting transition perturbations onto at least one realistic external environment such as mobile, coding, or long-horizon tool use;
5. statistical uncertainty and paired tests on the matched transitions;
6. comparisons to native permission systems and deterministic authorization gates.

The repository contains the infrastructure for these experiments, but this release does not fabricate their outputs.

## v1.2 adversarial hardening: scope-bound grants

The original transition suite revealed stale/static authority, but `latest_state` and the explicit state machine both reached 100%. That leaves a shortcut: treating authorization as a free-floating current label. v1.2 adds 1,080 trajectories where a grant is tied to a concrete action scope/version. Material task changes and delayed confirmations can therefore make the newest visible grant stale for the current action.

This addition sharpens the object of study from **dynamic authorization labels** to **dynamic, scope-bound authorization provenance**. In the synthetic mechanism test, a latest-label policy falls to 88.9% exact and executes under stale scope on 11.1% of steps, while a scope-aware state machine remains perfect. This remains instrument validation, not frontier-model evidence.
