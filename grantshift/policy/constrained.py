from __future__ import annotations
from dataclasses import dataclass
from grantshift.types import AgentState, Action, Decision
from grantshift.risk.estimator import estimate_risk


@dataclass
class ConstrainedInterventionPolicy:
    """Rank learned actions *inside* an explicit authorization/recoverability envelope.

    Unlike a post-hoc override, this policy masks inadmissible actions first and then
    chooses the highest-probability remaining action. This separates the permission
    channel (what may be done) from the preference channel (what the user tends to
    prefer among allowed options).
    """
    base_policy: object

    def admissible(self, state: AgentState) -> set[Action]:
        auth = str(state.metadata.get('authorization', 'advisory'))
        recoverable = bool(state.metadata.get('recoverable', state.reversibility >= 0.5))
        if auth == 'prohibited':
            allowed = {Action.DO_NOTHING, Action.WAIT, Action.DEFER}
        elif auth == 'ask_required':
            allowed = {Action.ASK, Action.SUGGEST, Action.WAIT, Action.DEFER, Action.DO_NOTHING}
        elif auth == 'preauthorized':
            allowed = set(Action)
        else:  # advisory
            allowed = {Action.ASK, Action.SUGGEST, Action.REMIND, Action.WAIT, Action.DEFER, Action.DO_NOTHING}
        if not recoverable:
            allowed.discard(Action.ACT)
        return allowed

    def decide(self, state: AgentState) -> Decision:
        allowed = self.admissible(state)
        if hasattr(self.base_policy, 'predict_proba'):
            probs = self.base_policy.predict_proba(state)
            candidates = {a: p for a, p in probs.items() if a in allowed}
            if candidates:
                action = max(candidates, key=candidates.get)
                confidence = candidates[action]
                top = sorted(candidates.items(), key=lambda kv: kv[1], reverse=True)[:3]
                reasons = [f'constrained rank: {a.value}={p:.2f}' for a,p in top]
                reasons.append('authorization/recoverability envelope applied before ranking')
                risk = estimate_risk(state)
                return Decision(action=action, utility=state.expected_benefit-risk, risk=risk, reasons=reasons, confidence=confidence)
        base = self.base_policy.decide(state)
        if base.action in allowed:
            return base
        # Conservative fallback if the base policy exposes no distribution.
        fallback = Action.ASK if Action.ASK in allowed else (Action.SUGGEST if Action.SUGGEST in allowed else Action.DO_NOTHING)
        return Decision(action=fallback, utility=base.utility, risk=base.risk,
                        reasons=list(base.reasons)+['constrained fallback to admissible action'], confidence=base.confidence)
