from __future__ import annotations

from dataclasses import dataclass

from grantshift.types import AgentState, Action, Decision


@dataclass
class AuthorizationFirstPolicy:
    """Constrain a personalized policy by explicit authorization and recoverability.

    Personalization is allowed to choose *within* the user's authorization envelope,
    but may not expand that envelope. This wrapper is deliberately simple and
    auditable: it encodes a precedence rule rather than hiding it inside a learned
    score.
    """

    base_policy: object

    def decide(self, state: AgentState) -> Decision:
        base = self.base_policy.decide(state)
        authorization = str(state.metadata.get("authorization", "advisory"))
        recoverable = bool(state.metadata.get("recoverable", state.reversibility >= 0.5))
        action = base.action
        reasons = list(base.reasons)

        # Explicit prohibition dominates all learned personalization.
        if authorization == "prohibited":
            action = Action.DO_NOTHING
            reasons.append("authorization-first: explicit prohibition -> do_nothing")

        # If user authorization requires confirmation, preserve initiative but
        # downgrade any stronger/non-consensual intervention to a question.
        elif authorization == "ask_required" and action not in {Action.ASK, Action.SUGGEST}:
            action = Action.ASK
            reasons.append("authorization-first: confirmation required -> ask")

        # Irreversible execution is never taken directly by this release policy.
        elif not recoverable and action == Action.ACT:
            action = Action.ASK
            reasons.append("authorization-first: low recoverability -> ask")

        return Decision(
            action=action,
            utility=base.utility,
            risk=base.risk,
            reasons=reasons,
            confidence=base.confidence,
        )
