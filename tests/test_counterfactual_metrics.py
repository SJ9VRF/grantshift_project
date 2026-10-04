from grantshift.types import Action, AgentState, ScenarioLabel
from evaluation.counterfactual import authorization_counterfactual_metrics


def state(auth, sid):
    return AgentState(
        scenario_id=sid, domain='test', goal='x', urgency=.5, intent_confidence=.8,
        execution_confidence=.8, stakes=.5, reversibility=.8, expected_benefit=.8,
        metadata={'authorization':auth,'frontier_group':'g1'}
    )


def label(a):
    return ScenarioLabel(preferred_action=a, acceptable_actions=[a], bad_actions=[], severity_of_wrong_action=.5)


def test_monotonic_authority_group():
    states=[state('prohibited','1'),state('advisory','2'),state('ask_required','3'),state('preauthorized','4')]
    preds=[Action.DO_NOTHING,Action.SUGGEST,Action.ASK,Action.ACT]
    labels=[label(a) for a in preds]
    m=authorization_counterfactual_metrics(states,preds,labels)
    assert m['all_four_exact_group_rate']==1.0
    assert m['authorization_ceiling_violation_rate']==0.0
    assert m['authority_monotonic_group_rate']==1.0


def test_ceiling_violation_detected():
    states=[state('prohibited','1')]
    preds=[Action.ACT]
    labels=[label(Action.DO_NOTHING)]
    m=authorization_counterfactual_metrics(states,preds,labels)
    assert m['authorization_ceiling_violation_rate']==1.0
