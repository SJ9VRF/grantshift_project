from pathlib import Path

from evaluation.metrics import evaluate
from grantshift.policy.heuristic import decide
from grantshift.types import Action
from grantshiftbench.loaders.jsonl import load_jsonl


def test_high_cost_travel_requires_user_control():
    path = Path(__file__).resolve().parents[1] / "grantshiftbench/scenarios/v0.jsonl"
    states, _ = load_jsonl(path)
    s = next(x for x in states if x.scenario_id == "travel_002")
    assert decide(s).action in {Action.ASK, Action.SUGGEST}


def test_low_value_nonurgent_case_stays_silent():
    path = Path(__file__).resolve().parents[1] / "grantshiftbench/scenarios/v0.jsonl"
    states, _ = load_jsonl(path)
    s = next(x for x in states if x.scenario_id == "prod_001")
    assert decide(s).action == Action.DO_NOTHING


def test_eval_runs():
    path = Path(__file__).resolve().parents[1] / "grantshiftbench/scenarios/v0.jsonl"
    states, labels = load_jsonl(path)
    result = evaluate([decide(s).action for s in states], labels)
    assert 0.0 <= result.acceptable_action_rate <= 1.0


def test_private_data_requires_ask():
    path = Path(__file__).resolve().parents[1] / "grantshiftbench/scenarios/v0.jsonl"
    states, _ = load_jsonl(path)
    s = next(x for x in states if x.scenario_id == "privacy_001")
    assert decide(s).action == Action.ASK


def test_explicit_reminder_preference_is_respected():
    path = Path(__file__).resolve().parents[1] / "grantshiftbench/scenarios/v0.jsonl"
    states, _ = load_jsonl(path)
    s = next(x for x in states if x.scenario_id == "routine_001")
    assert decide(s).action == Action.REMIND
