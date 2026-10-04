# Problem Formulation: Calibrated Proactivity

## Research question

How can a personal AI decide **when to act, ask, suggest, remind, wait, defer, or stay silent** while balancing goal progress, uncertainty, user autonomy, risk, timing, and individual preferences?

## Decision process

At time `t`, the agent observes a user-conditioned state `s_t` and chooses:

`a_t ∈ {ACT, ASK, SUGGEST, REMIND, WAIT, DEFER, DO_NOTHING}`.

The policy is explicitly user-conditioned:

`π(a | s, u)` rather than `π(a | s)`.

This distinction is central: identical situations can warrant different actions for users with different autonomy and interruption preferences.

## Utility

We optimize a multi-objective utility rather than intervention frequency:

`U(a | s, u) = B - λ_i I - λ_r R - λ_a A - λ_c C`

where:

- `B`: expected goal benefit
- `I`: intrusiveness / interruption cost
- `R`: action risk
- `A`: autonomy violation cost
- `C`: financial/social/privacy cost

The optimal action is:

`a* = argmax_a E[U(a | s, u)]`.

High uncertainty should shift behavior toward information-preserving actions such as `ASK`, rather than autonomous `ACT`.

## Two kinds of confidence

The project separates:

1. **Intent confidence** — confidence that the inferred goal or desired outcome is correct.
2. **Execution confidence** — confidence that the proposed action can be executed correctly.

These can diverge. High intent confidence with low execution confidence should often yield `ASK` or `SUGGEST`, not `ACT`.

## Error asymmetry

False proactivity and missed opportunities have different costs. A useful agent must optimize both:

- avoid needless or intrusive intervention;
- avoid silence when intervention would materially protect a user goal.

Therefore evaluation must measure not only what the agent does, but also what it correctly chooses **not** to do.

## Core hypotheses

- H1: Personalized policies outperform generic policies on acceptable-action rate and user utility.
- H2: Explicit risk modeling reduces autonomy violations without causing excessive passivity.
- H3: Confidence calibration lowers harmful autonomous actions under ambiguity.
- H4: A multi-action policy outperforms binary act/do-not-act formulations because `ASK`, `SUGGEST`, and `REMIND` provide intermediate autonomy-preserving actions.
- H5: Longitudinal adaptation improves intervention precision as the system learns user-specific tolerance and autonomy preferences.
