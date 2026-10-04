from grantshift.risk.estimator import estimate_risk
from grantshift.types import Action, AgentState, Decision


def decide(state: AgentState) -> Decision:
    """Transparent rule-based baseline for calibrated proactivity."""
    risk = estimate_risk(state)
    joint_confidence = min(state.intent_confidence, state.execution_confidence)
    preferred = state.user_profile.preference_for(state.domain)
    reasons = []

    if state.expected_benefit < 0.25 and state.urgency < 0.35:
        return Decision(
            action=Action.DO_NOTHING,
            utility=state.expected_benefit - risk,
            risk=risk,
            reasons=["Low expected benefit and low urgency"],
            confidence=joint_confidence,
        )

    if (state.privacy_risk >= 0.80 or state.financial_cost >= 0.80 or state.stakes >= 0.85) and preferred != Action.ACT:
        reasons.append("Sensitive or high-stakes action requires preserving user control")
        return Decision(Action.ASK, state.expected_benefit - risk, risk, reasons, joint_confidence)

    if risk >= 0.60:
        reasons.append("High estimated action risk")
        if state.urgency >= 0.75:
            reasons.append("High urgency makes silence costly")
            return Decision(Action.ASK, state.expected_benefit - risk, risk, reasons, joint_confidence)
        return Decision(Action.SUGGEST, state.expected_benefit - risk, risk, reasons, joint_confidence)

    if joint_confidence < 0.60:
        reasons.append("Intent or execution confidence is low")
        return Decision(Action.ASK, state.expected_benefit - risk, risk, reasons, joint_confidence)

    if preferred == Action.DO_NOTHING and state.urgency < 0.85:
        reasons.append("User profile strongly prefers non-intervention")
        return Decision(Action.DO_NOTHING, state.expected_benefit - risk, risk, reasons, joint_confidence)

    if preferred == Action.ACT and risk < 0.30 and joint_confidence >= 0.85:
        reasons.extend(["User permits autonomous action", "Low risk and high confidence"])
        return Decision(Action.ACT, state.expected_benefit - risk, risk, reasons, joint_confidence)

    if preferred == Action.REMIND and state.expected_benefit >= 0.40 and state.time_sensitivity >= 0.50:
        reasons.append("Explicit reminder preference matches a timely opportunity")
        return Decision(Action.REMIND, state.expected_benefit - risk, risk, reasons, joint_confidence)

    if state.urgency >= 0.80 and state.expected_benefit >= 0.60:
        if preferred == Action.REMIND:
            reasons.append("Urgent, beneficial, and reminder is user-preferred")
            return Decision(Action.REMIND, state.expected_benefit - risk, risk, reasons, joint_confidence)
        reasons.append("Urgent high-benefit opportunity")
        return Decision(Action.SUGGEST, state.expected_benefit - risk, risk, reasons, joint_confidence)

    if state.time_sensitivity < 0.30 and state.urgency < 0.45:
        reasons.append("Opportunity is not time-sensitive")
        return Decision(Action.WAIT, state.expected_benefit - risk, risk, reasons, joint_confidence)

    reasons.append("Moderate-risk opportunity; preserve user control")
    return Decision(Action.SUGGEST, state.expected_benefit - risk, risk, reasons, joint_confidence)
