# GrantShift - Technical Narrative for Research Interviews

## 30-second version

I built GrantShift to test a failure mode in personalized agents that standard task success can hide: preference can stay stable while authority changes. I started with a matched preference/permission benchmark, found that a simple latest-label policy could game the first transition suite, then deliberately falsified my own benchmark with scope-bound and provenance-bound adversarial tests. The strongest synthetic result is not a high score; it is that a policy that looked perfect on the easy suite falls to 66.7% when grants are bound to principal, request, resource, and revision, with 33.3% invalid-provenance execution. The repo includes trajectory graders, repeated trials, failure mining, a frontier-model run contract, and explicit claim-evidence gating.

## What I would emphasize to a research manager

The project demonstrates a research loop rather than a static benchmark:

**hypothesis -> controlled eval -> shortcut discovered -> adversarial falsification -> stronger state representation -> reliability measurement -> failure mining -> external-eval plan.**

The key design choice is to keep personalization evidence fixed while changing authorization, which isolates a causal factor that otherwise gets mixed with preference drift or generic context change.

## What I would not claim

I would not call the current numbers frontier-model SOTA. The 100% state-machine results are deterministic mechanism checks. The next meaningful experiment is to run the 1,602 unique frontier prompts across pinned frontier models, expand to the weighted 8,892-record benchmark, and report cluster-aware uncertainty and family-specific failures.

## Deep-dive question: why not just enforce permissions outside the model?

For hard, machine-readable permissions, deterministic enforcement is preferable. GrantShift targets the behavioral layer around incomplete, delayed, changing, or scope-sensitive authority: deciding whether a confirmation still applies, whether a material task revision invalidates consent, whether a reply belongs to the current request, and whether the assistant should ask, wait, or abstain. The benchmark is useful both for model behavior and for checking whether a surrounding policy layer has the right state representation.

## Deep-dive question: what did you learn by trying to break your own benchmark?

The first transition benchmark was too easy: reading the latest authorization label solved it. Scope-bound tests broke that shortcut. Provenance-bound tests were stronger still: they required matching principal, request, resource, and revision, and exposed replay/cross-wire failures. This changed the project thesis from “track permission changes” to “track the validity and provenance of authority over time.”
