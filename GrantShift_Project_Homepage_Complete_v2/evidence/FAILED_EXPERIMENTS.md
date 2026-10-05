# What Didn't Work

These are not invented failures. They are the negative results and design failures that materially changed GrantShift.

## 1. Oracle-visible structured factors
**Failure.** Early high accuracy was too easy because the evaluated representation exposed variables closely related to the synthetic gold rule.
**Why it failed scientifically.** It tested rule recovery more than agent reasoning.
**Change.** Latent factors were removed from model input; inputs and gold metadata were separated.

## 2. Canonical templates generalized poorly
**Failure.** ~98.7% canonical exact dropped to ~52.8% on held-out paraphrases.
**Why.** The classifier exploited surface regularities.
**Change.** Train-only surface augmentation plus explicit paraphrase stress testing.

## 3. Static authorization-first repeated ASK
**Failure.** Under delayed confirmation the policy kept asking rather than tracking a pending confirmation.
**Why.** Authorization was treated as a rule, not evolving interaction state.
**Change.** Stateful pending-confirmation representation.

## 4. Latest-label tracking looked perfect
**Failure.** The first transition benchmark could not distinguish latest-label tracking from a real state machine.
**Why.** Grants were not bound tightly enough to the action being authorized.
**Change.** Scope/version-bound adversarial transitions.

## 5. Flat provenance was still insufficient
**Failure.** Matching principal/request/resource/revision still failed under expiry and delegation ancestry.
**Why.** Provenance without lifecycle history treats capability validity as a flat tuple.
**Change.** Capability ledger with expiry, revocation, ancestry, nonce and replay state.

## 6. Our first ledger recovery rule was too permissive
**Failure.** A revoked delegated token could fall through to ASK.
**Why.** Generic recovery conflated stale/revoked authority with absence of authority.
**Change.** Explicit revoked-token invariant and principal-change distinction.

## 7. The benchmark itself had blind spots
**Failure.** Mutation testing showed that removing nonce, request, principal, resource or revision binding could initially pass without regression.
**Why.** Existing scenarios composed several factors but did not isolate each invariant.
**Change.** Added direct isolation families; release now gates on all targeted mutants being detected.

## What we deliberately did not “fix” with a claim
No frontier-model, human, or production result exists yet. The repository contains harnesses for those evidence levels, but infrastructure is not reported as empirical success.
