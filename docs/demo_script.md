# Three-Minute Demo Script

## 0:00–0:25 — Frame the problem
Show the dashboard title and say: “Most assistants are evaluated after the user asks. This system studies the decision before that: should the agent act, ask, suggest, remind, wait, defer, or stay silent?”

## 0:25–1:05 — Same situation, different users
Open two matched personalization scenarios with the same opportunity state. For the autonomy-first user, show `ASK` or `SUGGEST`; for a delegator in a safe/reversible context, show `ACT`.

Run `python demo/decision_trace.py` and point to risk, confidence, user preference, chosen action, and alternatives.

Message: the policy is user-conditioned, not a universal aggressiveness threshold.

## 1:05–1:40 — High-stakes guardrail
Show a financial/privacy/high-stakes scenario. Increase benefit and urgency while keeping reversibility low. The system should preserve user control rather than treating urgency as permission.

Explain the distinction between “I think this is useful” and “I am authorized to do it.”

## 1:40–2:10 — Preference drift
Show the longitudinal result: frozen preference is correct before the update and wrong after it, while the adaptive state follows the change.

Message: personal agents need temporal user models, not just memory retrieval.

## 2:10–2:40 — Evals
Open the dashboard. Highlight exact accuracy, false proactivity, missed opportunity, autonomy violations, calibration, and domain-level weaknesses.

Point out that calibration is fitted on the dev split and evaluated once on test.

## 2:40–3:00 — Research boundary
End on the limitation: “These labels are a transparent synthetic oracle. I built the full reproducible research machinery, but I do not present synthetic agreement as human evidence. The next stage is human annotation and longitudinal external-agent evaluation.”
