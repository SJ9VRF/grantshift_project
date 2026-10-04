import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def test_mutation_gate_detects_every_targeted_invariant():
    p=ROOT/'artifacts/capability_mutation_eval.json'
    assert p.exists()
    x=json.loads(p.read_text())
    assert x['release_gate']['all_targeted_mutants_detected'] is True
    expected={
        'ignore_expiry','ignore_nonce_revocation','ignore_parent_revocation',
        'ignore_request_binding','ignore_principal_binding','ignore_resource_binding','ignore_revision_binding'
    }
    assert expected <= set(x['mutants'])
    for name in expected:
        assert x['mutants'][name]['exact_drop_vs_reference'] > 0
        assert x['mutants'][name]['invalid_capability_execution_rate'] > 0

def test_capability_challenge_isolation_families_present():
    meta=json.loads((ROOT/'grantshiftbench/capability_ledger/metadata.json').read_text())
    required={'direct_nonce_revoked','request_changed_old_grant','principal_mismatch_grant','resource_mismatch_grant','revision_mismatch_grant'}
    assert required <= set(meta['families'])
    assert meta['n_trajectories']==1440
    assert meta['n_steps']==5760
