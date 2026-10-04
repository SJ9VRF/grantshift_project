from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class Action(str, Enum):
    ACT = "act"
    ASK = "ask"
    SUGGEST = "suggest"
    REMIND = "remind"
    WAIT = "wait"
    DEFER = "defer"
    DO_NOTHING = "do_nothing"


@dataclass
class AutonomyProfile:
    domain_preferences: Dict[str, Action] = field(default_factory=dict)
    interruption_tolerance: float = 0.5
    default_action: Action = Action.ASK

    def preference_for(self, domain: str) -> Action:
        return self.domain_preferences.get(domain, self.default_action)


@dataclass
class AgentState:
    scenario_id: str
    domain: str
    goal: str
    urgency: float
    intent_confidence: float
    execution_confidence: float
    stakes: float
    reversibility: float
    expected_benefit: float
    financial_cost: float = 0.0
    social_cost: float = 0.0
    privacy_risk: float = 0.0
    safety_risk: float = 0.0
    time_sensitivity: float = 0.0
    user_profile: AutonomyProfile = field(default_factory=AutonomyProfile)
    metadata: Dict[str, object] = field(default_factory=dict)


@dataclass
class Decision:
    action: Action
    utility: float
    risk: float
    reasons: List[str]
    confidence: float


@dataclass
class ScenarioLabel:
    preferred_action: Action
    acceptable_actions: List[Action]
    bad_actions: List[Action]
    severity_of_wrong_action: float
