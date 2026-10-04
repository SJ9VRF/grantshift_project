import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def test_robustness_artifact_exists_and_is_coherent():
    p=ROOT/'artifacts/v2_robustness_suite.json'
    assert p.exists()
    d=json.loads(p.read_text())
    assert d['metadata']['test_n']==900
    assert d['negative_controls']['authorization_shuffled']['exact'] < d['canonical']['exact']
    assert d['negative_controls']['authorization_masked']['unauthorized_act_rate'] > d['canonical']['unauthorized_act_rate']
    assert d['surface_augmentation']['paraphrase']['exact'] > d['paraphrase']['exact']
    assert len(d['train_subsample_robustness']['runs'])==5
    assert set(d['leave_one_domain_out'])=={'calendar','communication','email','files','productivity','shopping','travel'}

def test_surface_augmentation_uses_train_bases_only():
    split=json.loads((ROOT/'grantshiftbench/v2/factorial_splits.json').read_text())
    assert set(split['train']).isdisjoint(set(split['test']))
