from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from sklearn.linear_model import LogisticRegression
from grantshift.types import Action, AgentState

ACTIONS=list(Action)

def _state_vector(s: AgentState):
    return np.array([
        1.0, s.expected_benefit, s.urgency, s.intent_confidence, s.execution_confidence,
        s.stakes, s.reversibility, s.financial_cost, s.social_cost, s.privacy_risk,
        s.safety_risk, s.time_sensitivity, s.user_profile.interruption_tolerance,
    ], dtype=float)

def _phi(state: AgentState, action: Action):
    # Block-coded state × action interactions let the reward change by action and context.
    sv=_state_vector(state)
    blocks=[]
    pref=state.user_profile.preference_for(state.domain)
    for a in ACTIONS:
        if a==action:
            blocks.extend(sv)
            blocks.extend([float(action==pref), float(action==Action.ACT and state.reversibility<.5), float(action==Action.ACT and max(state.stakes,state.financial_cost,state.privacy_risk,state.safety_risk)>.8)])
        else:
            blocks.extend(np.zeros(len(sv)+3))
    return np.asarray(blocks,dtype=float)

@dataclass
class PairwiseRewardModel:
    model: LogisticRegression | None = None
    def fit(self, pairs):
        X=[]; y=[]
        for s,chosen,rejected in pairs:
            d=_phi(s,chosen)-_phi(s,rejected)
            X.extend([d,-d]); y.extend([1,0])
        self.model=LogisticRegression(max_iter=3000, C=1.0).fit(X,y)
        return self
    def score(self,state,action):
        if self.model is None: raise RuntimeError("not fit")
        return float(self.model.decision_function([_phi(state,action)])[0])
    def decide(self,state):
        return max(ACTIONS,key=lambda a:self.score(state,a))
