from grantshift.policy.frontier import AuthorizationFirstPolicy
from grantshift.types import AgentState, AutonomyProfile, Action, Decision

class Stub:
    def __init__(self, action): self.action=action
    def decide(self, state):
        return Decision(self.action, utility=0.5, risk=0.1, reasons=['stub'], confidence=0.9)

def state(auth='advisory', recoverable=True):
    return AgentState(
        scenario_id='x', domain='calendar', goal='g', urgency=.8,
        intent_confidence=.9, execution_confidence=.9, stakes=.5,
        reversibility=.9 if recoverable else .1, expected_benefit=.8,
        user_profile=AutonomyProfile(),
        metadata={'authorization': auth, 'recoverable': recoverable},
    )

def test_prohibited_dominates_personalization():
    assert AuthorizationFirstPolicy(Stub(Action.ACT)).decide(state('prohibited')).action == Action.DO_NOTHING

def test_confirmation_required_downgrades_act():
    assert AuthorizationFirstPolicy(Stub(Action.ACT)).decide(state('ask_required')).action == Action.ASK

def test_irreversible_act_downgrades_to_ask():
    assert AuthorizationFirstPolicy(Stub(Action.ACT)).decide(state('preauthorized', False)).action == Action.ASK

def test_advisory_suggestion_is_preserved():
    assert AuthorizationFirstPolicy(Stub(Action.SUGGEST)).decide(state('advisory')).action == Action.SUGGEST
