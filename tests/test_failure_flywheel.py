import json
from pathlib import Path
from posttraining.failure_mining import classify
from posttraining.reward import trajectory_reward
from evaluation.grader_calibration import binary_calibration

ROOT=Path(__file__).resolve().parents[1]

def test_executed_incident_bank_and_training_pairs_exist():
    assert (ROOT/'artifacts/incident_bank.json').exists()
    incidents=json.loads((ROOT/'artifacts/incident_bank.json').read_text())
    assert incidents
    text=(ROOT/'artifacts/failure_training_pairs.jsonl').read_text().strip().splitlines()
    assert len(text)==len(incidents)


def test_reward_strongly_penalizes_authorization_failure():
    safe={"trajectory":[{}],"graders":[
      {"grader":"authorization","score":1},{"grader":"outcome","score":1},
      {"grader":"recovery","score":1},{"grader":"interaction_efficiency","score":1}]}
    unsafe={"trajectory":[{}],"graders":[
      {"grader":"authorization","score":0},{"grader":"outcome","score":1},
      {"grader":"recovery","score":1},{"grader":"interaction_efficiency","score":1}]}
    assert trajectory_reward(safe) - trajectory_reward(unsafe) >= 5.0


def test_grader_calibration_math():
    r=binary_calibration([1,1,0,0,1],[1,0,0,0,1])
    assert r.n==5
    assert 0 <= r.cohen_kappa <= 1
    assert abs(r.accuracy-.8)<1e-9
