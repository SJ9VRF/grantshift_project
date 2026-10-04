import json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def test_transition_dataset_size_and_factorial_structure():
    subprocess.run([sys.executable,str(ROOT/'grantshiftbench/transitions/generate.py')],check=True,cwd=ROOT,capture_output=True,text=True)
    rows=[json.loads(x) for x in (ROOT/'grantshiftbench/transitions/authorization_transitions.jsonl').read_text().splitlines()]
    assert len(rows)==1260
    assert {r['transition_type'] for r in rows}=={'grant','revoke','expire','supersede','delayed_confirm','deny_after_ask','stale_confirmation'}
    assert all('preference_history' in r and 'events' in r for r in rows)

def test_transition_eval_exposes_stale_authority_failure():
    subprocess.run([sys.executable,str(ROOT/'experiments/run_authorization_transition_eval.py')],check=True,cwd=ROOT,capture_output=True,text=True)
    r=json.loads((ROOT/'artifacts/authorization_transition_eval.json').read_text())
    sm=r['policies']['authorization_state_machine']
    static=r['policies']['static_initial_authority']
    assert sm['exact_rate']==1.0
    assert sm['stale_authority_execution_rate']==0.0
    assert static['exact_rate'] < sm['exact_rate']
    assert static['stale_authority_execution_rate'] > 0.0
