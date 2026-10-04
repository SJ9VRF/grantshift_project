from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

import joblib

from grantshift.policy.learned import LearnedPolicy
from grantshift.types import Action, AgentState, AutonomyProfile


def save_policy(policy: LearnedPolicy, path: str | Path, metadata: dict[str, Any] | None = None) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "format_version": 1,
        "policy": policy,
        "metadata": metadata or {},
    }
    joblib.dump(payload, path)
    return path


def load_policy(path: str | Path) -> tuple[LearnedPolicy, dict[str, Any]]:
    payload = joblib.load(path)
    if not isinstance(payload, dict) or payload.get("format_version") != 1:
        raise ValueError("unsupported policy bundle")
    policy = payload.get("policy")
    if not isinstance(policy, LearnedPolicy):
        raise TypeError("bundle does not contain a LearnedPolicy")
    return policy, dict(payload.get("metadata", {}))


def state_from_dict(raw: dict[str, Any]) -> AgentState:
    profile_raw = raw.get("user_profile", {}) or {}
    profile = AutonomyProfile(
        domain_preferences={k: Action(v) for k, v in profile_raw.get("domain_preferences", {}).items()},
        interruption_tolerance=float(profile_raw.get("interruption_tolerance", 0.5)),
        default_action=Action(profile_raw.get("default_action", "ask")),
    )
    return AgentState(
        scenario_id=str(raw.get("scenario_id", "cli")),
        domain=str(raw["domain"]),
        goal=str(raw["goal"]),
        urgency=float(raw["urgency"]),
        intent_confidence=float(raw["intent_confidence"]),
        execution_confidence=float(raw["execution_confidence"]),
        stakes=float(raw["stakes"]),
        reversibility=float(raw["reversibility"]),
        expected_benefit=float(raw["expected_benefit"]),
        financial_cost=float(raw.get("financial_cost", 0.0)),
        social_cost=float(raw.get("social_cost", 0.0)),
        privacy_risk=float(raw.get("privacy_risk", 0.0)),
        safety_risk=float(raw.get("safety_risk", 0.0)),
        time_sensitivity=float(raw.get("time_sensitivity", 0.0)),
        user_profile=profile,
        metadata=dict(raw.get("metadata", {})),
    )


def state_to_dict(state: AgentState) -> dict[str, Any]:
    raw = asdict(state)
    raw["user_profile"]["domain_preferences"] = {
        k: v.value for k, v in state.user_profile.domain_preferences.items()
    }
    raw["user_profile"]["default_action"] = state.user_profile.default_action.value
    return raw


def read_state(path: str | Path) -> AgentState:
    return state_from_dict(json.loads(Path(path).read_text()))
