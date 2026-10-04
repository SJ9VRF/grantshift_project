# Reviewer-facing evidence checklist

## Claims supported by executed artifacts
- Preference and authorization are independently manipulated in a 3 x 4 factorial design.
- Counterfactual siblings are grouped by base scenario before train/dev/test splitting.
- Evaluated model inputs exclude structured latent fields and expose natural-language evidence only.
- Trivial policies (always ask, always act, always silent, always suggest) are evaluated explicitly.
- The release measures unauthorized autonomous action, question burden, unnecessary intervention, missed opportunity, and synthetic utility.
- A held-out surface-form paraphrase test exposes substantial template sensitivity.
- A 100-turn synthetic drift simulation measures stale-preference failure and adaptation latency.
- Utility conclusions are stress-tested over a grid of ask costs and overreach penalties.

## Claims intentionally NOT made
- No claim that synthetic gold equals human preference.
- No claim of state-of-the-art frontier-model performance.
- No claim of real-world deployment safety.
- No claim that the classical baseline is a production agent.
- No claim that the synthetic drift simulator establishes longitudinal human behavior.

## Evidence still required for a strong external submission
- Human validation with agreement and individual-level labels.
- Frontier-model comparison on the blinded prompt set.
- Audit of realistic external tasks/benchmarks under matched permission counterfactuals.
- Interactive consequence study with real tool actions in a sandbox.
