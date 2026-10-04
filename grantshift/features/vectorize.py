from __future__ import annotations

from dataclasses import asdict
from grantshift.types import AgentState

NUMERIC = [
    "urgency","intent_confidence","execution_confidence","stakes","reversibility",
    "expected_benefit","financial_cost","social_cost","privacy_risk","safety_risk","time_sensitivity"
]

def state_to_record(state: AgentState, include_personalization: bool = True, feature_groups: set[str] | None = None) -> dict:
    groups = feature_groups or {"core","risk","personalization","context"}
    r = {}
    if "core" in groups:
        for k in ["urgency","intent_confidence","execution_confidence","expected_benefit","time_sensitivity"]:
            r[k] = getattr(state,k)
    if "risk" in groups:
        for k in ["stakes","reversibility","financial_cost","social_cost","privacy_risk","safety_risk"]:
            r[k] = getattr(state,k)
    if "context" in groups:
        r["domain"] = state.domain
        r["goal"] = state.goal
        r["trigger"] = str(state.metadata.get("trigger","unknown"))
        r["authorization"] = str(state.metadata.get("authorization","advisory"))
        r["recoverable"] = str(bool(state.metadata.get("recoverable", state.reversibility >= 0.65)))
    if include_personalization and "personalization" in groups:
        pref = state.user_profile.preference_for(state.domain)
        r["user_domain_preference"] = pref.value
        r["user_default_action"] = state.user_profile.default_action.value
        r["interruption_tolerance"] = state.user_profile.interruption_tolerance
        r["profile_id"] = str(state.metadata.get("profile_id","unknown"))
        r["explicit_instruction"] = str(state.metadata.get("explicit_instruction","none"))
    return r
