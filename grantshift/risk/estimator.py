from grantshift.types import AgentState


def estimate_risk(state: AgentState) -> float:
    """Simple bounded baseline risk estimator.

    This is intentionally transparent: later experiments can replace it with a
    learned estimator while preserving the same interface.
    """
    irreversibility = 1.0 - state.reversibility
    raw = (
        0.25 * state.stakes
        + 0.20 * irreversibility
        + 0.15 * state.financial_cost
        + 0.15 * state.social_cost
        + 0.15 * state.privacy_risk
        + 0.10 * state.safety_risk
    )
    return max(0.0, min(1.0, raw))
