# Experiment Summary

All numbers below are from a deterministic **synthetic-oracle benchmark**. They validate the research machinery and controlled causal contrasts; they are not evidence of human preference validity.

## Main held-out test split

| Model | Exact | 95% bootstrap CI | Acceptable | False proactive | Missed opportunity | Autonomy violation | Top-label ECE |
|---|---:|---:|---:|---:|---:|---:|---:|
| heuristic | 0.741 | [0.647, 0.824] | 0.941 | 0.065 | 0.019 | 0.000 | 0.207 |
| generic learned | 0.871 | [0.800, 0.941] | 0.976 | 0.000 | 0.019 | 0.000 | 0.112 |
| personalized learned | 0.929 | [0.871, 0.976] | 0.976 | 0.000 | 0.019 | 0.000 | 0.039 |
| personalized calibrated | 0.929 | [0.871, 0.976] | 0.976 | 0.000 | 0.019 | 0.000 | 0.037 |

The calibrated policy fits a single scalar temperature on the **held-out development split** and then evaluates once on test. This avoids calibrating on the evaluation set.
Selected temperature: **0.891**.

## Contrastive personalization set

The same underlying opportunity states are paired with different user autonomy profiles. This isolates whether user-conditioned information changes the intervention decision.

| Model | Exact | False proactive |
|---|---:|---:|
| Generic | 0.512 | 1.000 |
| Personalized | 0.925 | 0.077 |

## Matched intervention-frontier set

This 240-case set holds 60 base situations approximately fixed while counterfactually changing authorization. It exposes a failure hidden by IID personalization accuracy.

| Policy | Exact | Acceptable | False proactive | Mean overreach |
|---|---:|---:|---:|---:|
| Generic | 0.700 | 0.796 | 0.194 | 0.150 |
| Generic + authorization gate | 0.896 | 0.992 | 0.032 | 0.221 |
| Personalized, unconstrained | 0.504 | 0.562 | 0.806 | 0.442 |
| GrantShift authorization-first | 0.879 | 0.938 | 0.000 | 0.192 |
| GrantShift constrained ranker | 0.713 | 0.875 | 0.000 | 0.025 |

The authorization-first rule is explicit: **authorization > recoverability > personalization**.

## OOD stress tests

Held-out domains: personalized exact **0.867**, acceptable **0.993**.
Held-out triggers: personalized exact **0.817**, acceptable **0.900**, false-proactivity **1.000**. The trigger failure is intentionally retained.

## Selective intervention / calibrated restraint

Instead of forcing an intervention decision at every state, we can require a minimum calibrated confidence. This explicitly tests whether uncertainty can be converted into restraint.

| Confidence threshold | Coverage | Exact | Acceptable | Severity-weighted error |
|---:|---:|---:|---:|---:|
| 0.70 | 0.941 | 0.963 | 0.975 | 0.009 |
| 0.80 | 0.894 | 0.987 | 0.987 | 0.003 |
| 0.85 | 0.847 | 0.986 | 0.986 | 0.003 |
| 0.90 | 0.847 | 0.986 | 0.986 | 0.003 |

## Paired statistical diagnostics

Main generic→personalized exact delta: **0.059**, paired-bootstrap 95% CI **[0.000, 0.118]**, exact McNemar p=**0.125**.
Frontier unconstrained→authorization-first exact delta: **0.375**, 95% CI **[0.312, 0.437]**, exact McNemar p=**1.62e-27**.
These tests describe this deterministic synthetic benchmark; they do not establish population-level human significance.

## Local numeric perturbation stability

Action stability under ±0.01 normalized numeric jitter: **0.996**; under ±0.05 jitter: **0.991**. This is a sensitivity diagnostic, not a correctness claim.
## Pairwise preference/reward baseline

Exact accuracy: **0.835**  
Acceptable-action rate: **0.976**  
False-proactivity rate: **0.000**

## Preference drift

| Policy state | Pre-drift | Post-drift |
|---|---:|---:|
| Frozen | 1.000 | 0.000 |
| Adaptive | 1.000 | 1.000 |

## Interpretation boundary

The benchmark intentionally exposes controlled behavior differences, but it does not establish that the oracle's intervention preferences match real users. Publication-grade claims require blinded human annotation, inter-annotator agreement, natural-language scenario validation, and evaluation against external agent/model backends.
