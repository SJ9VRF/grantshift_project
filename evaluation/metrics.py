from dataclasses import dataclass
from typing import Iterable

from grantshift.types import Action, ScenarioLabel


INTERVENTIONS = {Action.ACT, Action.ASK, Action.SUGGEST, Action.REMIND}


@dataclass
class EvalResult:
    accuracy: float
    acceptable_action_rate: float
    false_proactivity_rate: float
    missed_opportunity_rate: float
    autonomy_violation_rate: float


def evaluate(predictions: Iterable[Action], labels: Iterable[ScenarioLabel]) -> EvalResult:
    preds = list(predictions)
    labs = list(labels)
    if len(preds) != len(labs):
        raise ValueError("predictions and labels must have equal length")
    if not preds:
        raise ValueError("cannot evaluate an empty set")

    correct = acceptable = false_proactive = missed = autonomy = 0
    non_intervention_gold = intervention_gold = 0

    for pred, label in zip(preds, labs):
        correct += pred == label.preferred_action
        acceptable += pred in label.acceptable_actions

        gold_needs_intervention = any(a in INTERVENTIONS for a in label.acceptable_actions)
        if gold_needs_intervention:
            intervention_gold += 1
            if pred not in INTERVENTIONS:
                missed += 1
        else:
            non_intervention_gold += 1
            if pred in INTERVENTIONS:
                false_proactive += 1

        if pred == Action.ACT and Action.ACT in label.bad_actions:
            autonomy += 1

    n = len(preds)
    return EvalResult(
        accuracy=correct / n,
        acceptable_action_rate=acceptable / n,
        false_proactivity_rate=false_proactive / non_intervention_gold if non_intervention_gold else 0.0,
        missed_opportunity_rate=missed / intervention_gold if intervention_gold else 0.0,
        autonomy_violation_rate=autonomy / n,
    )
