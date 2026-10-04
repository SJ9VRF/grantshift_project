# Claim-to-ablation matrix

This matrix is intentionally adversarial: each claim lists the experiment that could falsify it, not merely the result that supports it.

| Claim | Primary evidence | Falsifying / negative control | Current status |
|---|---|---|---|
| Preference evidence is not authorization | 6,000-case factorial C0-C3 study | Shuffle/mask authorization evidence | Supported only in the synthetic mechanism test |
| Dynamic authority must update behavior immediately | 1,260 transition trajectories | Freeze initial authority | Supported synthetically; frontier-model run pending |
| Reading only the latest authorization label is insufficient | 1,080 scope-bound adversarial trajectories | Latest-label policy vs scope-bound state machine | Supported synthetically; 88.9% vs 100% exact |
| Surface robustness matters | 900 unseen paraphrases | Canonical-only baseline | Supported synthetically; canonical baseline collapses on unseen phrasing |
| Repeated-run reliability is stricter than pass@1 | 2,880 trajectory trials + environment shifts | Seeded 8% action noise | Supported in sandbox only |
| Failure mining can produce post-training records | Incident bank -> chosen/rejected pairs | Remove incident severity/frequency prioritization | Pipeline demonstrated; no frontier post-training result claimed |
| GrantShift improves frontier agents | None yet | Real model A/B post-training comparison | **Unverified** |
| GrantShift matches human authorization judgments | Human-study protocol only | Participant labels / mixed-effects analysis | **Unverified** |

A release fails the claim-evidence audit if an externally unverified claim is promoted to an empirical conclusion.

| Authorization provenance is necessary, not only a latest label | 864 provenance-bound trajectories | Latest-label vs provenance-aware state machine | Supported synthetically; 66.7% vs 100% exact, 33.3% vs 0% invalid-provenance ACT |
