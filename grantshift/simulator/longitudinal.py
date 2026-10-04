from __future__ import annotations
from dataclasses import replace
import random
from grantshift.types import Action, AutonomyProfile, AgentState

class LongitudinalUserSimulator:
    def __init__(self, profile: AutonomyProfile, seed: int = 7):
        self.profile=profile
        self.rng=random.Random(seed)
        self.turn=0
        self.history=[]

    def drift(self, domain: str, new_action: Action, interruption_tolerance: float | None = None):
        self.profile.domain_preferences[domain]=new_action
        if interruption_tolerance is not None:
            self.profile.interruption_tolerance=interruption_tolerance

    def step(self, template: AgentState) -> tuple[AgentState, Action]:
        self.turn += 1
        state=replace(template, user_profile=self.profile)
        pref=self.profile.preference_for(state.domain)
        # synthetic oracle with risk/urgency overrides
        if state.stakes>=0.85 or state.financial_cost>=0.8 or state.privacy_risk>=0.8:
            target=Action.ASK if pref != Action.ACT else (Action.ACT if state.reversibility>=0.7 and state.intent_confidence>=0.9 else Action.ASK)
        elif state.expected_benefit<0.25 and state.urgency<0.35:
            target=Action.DO_NOTHING
        elif pref==Action.REMIND and state.time_sensitivity>=0.5:
            target=Action.REMIND
        elif pref==Action.ACT and state.reversibility>=0.7 and state.intent_confidence>=0.85 and state.execution_confidence>=0.85:
            target=Action.ACT
        elif pref==Action.DO_NOTHING and state.urgency<0.9:
            target=Action.DO_NOTHING
        elif state.intent_confidence<0.6:
            target=Action.ASK
        elif state.urgency>=0.8:
            target=Action.SUGGEST
        else:
            target=Action.WAIT if state.time_sensitivity<0.3 else Action.SUGGEST
        self.history.append((state,target))
        return state,target
