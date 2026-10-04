# GrantShift - Research Dossier

**Author:** Aura Yavary

## One-sentence thesis
Personalization is persistent, but authority is dynamic and capability-scoped; agents must track the validity of authorization across action revisions, expiry, replay, concurrency, and delegation rather than treating the latest permission label as globally transferable.

## What changed through falsification
- Static permission labels failed under transitions.
- Latest authorization state looked perfect on easy transitions but failed when grants were scope-bound.
- Flat provenance fixed request/resource confusion but still failed under expiry and delegation ancestry.
- A capability ledger that tracks lifecycle and revocation history closes those deterministic synthetic failures.

## Strongest current evidence
- 6,000 matched preference-by-authorization cases.
- 1,260 dynamic-authorization trajectories.
- 1,080 scope/version adversarial trajectories.
- 864 provenance trajectories.
- 1,440 compositional capability-ledger trajectories (5,760 steps), plus invariant-level mutation testing.
- Latest-label: 70% exact / 30% invalid capability execution.
- Flat provenance: 85% / 15%.
- Capability ledger: 100% / 0% on the deterministic instrument.

## What would falsify the project
If frontier models already track these capability transitions reliably across paraphrases and external interactive environments, or if human raters do not agree that the proposed stale-capability executions are invalid, the central empirical motivation weakens.

## What is deliberately not claimed
No frontier-model SOTA, no human-validity claim, no deployment-safety claim, and no production post-training improvement claim without external evidence.
