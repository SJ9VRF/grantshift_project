# Real Evaluation Tables

All values below come from repository artifacts. “Real” here means actually executed in this repository; it does **not** mean human/frontier/production evidence.

## Capability challenge
1,440 trajectories / 5,760 decision steps across 10 adversarial capability families.

| Variant | Exact | Invalid execution | N | Notes |
|---|---:|---:|---:|---|
| Latest authorization label | 72.5% | 27.5% | 5,760 steps | ignores lifecycle/provenance composition |
| Flat provenance | 90.0% | 10.0% | 5,760 steps | matches flat identity fields but misses lifecycle history |
| Capability ledger | 100.0% | 0.0% | 5,760 steps | deterministic reference mechanism |

## Mutation sensitivity
| Mutant | Exact | Invalid execution | Interpretation |
|---|---:|---:|---|
| Full reference ledger | 100.0% | 0.0% | reference |
| Ignore expiry | 95.0% | 5.0% | detected |
| Ignore nonce revocation | 97.5% | 2.5% | detected |
| Ignore parent revocation | 97.5% | 2.5% | detected |
| Ignore request binding | 97.5% | 2.5% | detected |
| Ignore principal binding | 97.5% | 2.5% | detected |
| Ignore resource binding | 97.5% | 2.5% | detected |
| Ignore revision binding | 97.5% | 2.5% | detected |

## Surface robustness
| Training/eval condition | Exact | Notes |
|---|---:|---|
| Canonical-only → canonical | ~98.7% | synthetic mechanism check |
| Canonical-only → held-out paraphrase | ~52.8% | severe surface shortcut |
| Train-only surface augmentation → paraphrase | ~99.0% | shortcut largely repaired |

For exact machine-readable values and any confidence intervals available for a specific suite, use the linked JSON artifacts rather than rounded values in this page.
