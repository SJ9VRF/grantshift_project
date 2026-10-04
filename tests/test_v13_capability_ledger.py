import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def test_capability_ledger_results_exist_and_separate_policies():
    r=json.loads((ROOT/'artifacts/capability_ledger_eval.json').read_text())
    assert r['n_trajectories']==1440
    assert r['policies']['latest_authorization_label']['exact_rate']==0.725
    assert r['policies']['flat_provenance']['exact_rate']==0.9
    assert r['policies']['capability_ledger']['exact_rate']==1.0
    assert r['policies']['capability_ledger']['invalid_capability_execution_rate']==0.0

def test_capability_ledger_statistics_are_clustered_and_paired():
    s=json.loads((ROOT/'artifacts/capability_ledger_statistics.json').read_text())
    assert s['unit']=='trajectory-cluster bootstrap'
    assert s['paired_vs_capability_ledger']['flat_provenance']['ledger_better']==576
    assert s['paired_vs_capability_ledger']['flat_provenance']['other_better']==0

def test_formal_spec_and_trace_explorer_are_public_artifacts():
    spec=json.loads((ROOT/'configs/authorization_state_machine.json').read_text())
    assert len(spec['invariants'])>=6
    page=(ROOT/'project/trace_explorer.html').read_text()
    assert 'GrantShift Trace Explorer' in page
    assert 'INVALID EXECUTION' in page
