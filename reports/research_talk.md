# 8–10 Minute Research Talk — GrantShift

## Slide 1 — The question (45 sec)
**When should an AI act?**

Open with the failure mode: an assistant can be capable and still be a bad personal agent if it interrupts too often, waits too long, or acts without permission.

Core line: *Proactivity is not just capability. It is judgment under uncertainty.*

## Slide 2 — Why binary act/don't-act is insufficient (45 sec)
Show the seven-action space: ACT, ASK, SUGGEST, REMIND, WAIT, DEFER, DO_NOTHING.

Use one high-stakes example: detecting a likely missed connection may justify an alert; purchasing a replacement flight may still require confirmation.

## Slide 3 — Formulation (60 sec)
Present the utility decomposition: expected benefit minus intrusion, risk, autonomy, and action cost.

Explain the two independent confidences: intent confidence and execution confidence.

## Slide 4 — Personalized architecture (60 sec)
Goal state → opportunity → risk → confidence → user autonomy profile → intervention policy → outcome/feedback.

Emphasize that the policy is \(\pi(a\mid s,u)\), not only \(\pi(a\mid s)\).

## Slide 5 — GrantShiftBench (60 sec)
600 main scenarios, 12 domains, 416/97/87 stratified shuffled train/dev/test, multi-valid labels, explicit bad actions and failure severity.

Then show the 160-example matched personalization set where the state is held approximately fixed and the user preference changes.

## Slide 6 — Evaluation beyond accuracy (60 sec)
Show useful-intervention precision/recall, false proactivity, missed opportunities, autonomy violations, ECE/Brier, severity, and per-domain regressions.

Line: *A proactive agent must get credit for correctly choosing silence.*

## Slide 7 — Results (75 sec)
Generic learned: 74.7% exact.
Personalized learned: 92.0% exact.
Held-out calibration: same 92.0% decisions, ECE 0.0706 → 0.0626.
Contrastive set: generic 53.8%, personalized 93.8%.

Immediately state the caveat: these are synthetic-oracle mechanism tests, not human preference claims.

## Slide 8 — Preference drift (45 sec)
Show frozen versus adaptive profile after a controlled preference reversal.

Message: memory can be correct historically and still be wrong now. Proactivity therefore depends on temporal user state, not static preference retrieval.

## Slide 9 — Failure analysis (60 sec)
Highlight communication/privacy/travel errors and the taxonomy: overreach, passivity, wrong modality, stale state, confidence failure, irreversible mistake.

Explain why preserving these failures is useful: they define the next research agenda.

## Slide 10 — Research direction (45 sec)
Human-labeled benchmark → natural conversations → external model/tool backends → longitudinal adaptive policy → post-training on real preference signals.

Close with: *The question for personal AI is not only “Can the model help?” It is “Does the model know when its involvement is actually valuable?”*
