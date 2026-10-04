from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
def load(p): return [json.loads(x) for x in Path(p).read_text().splitlines() if x.strip()]
def test_v2_size_and_blinding():
    xs=load(ROOT/'grantshiftbench/v2/factorial_inputs.jsonl'); gs=load(ROOT/'grantshiftbench/v2/factorial_gold.jsonl')
    assert len(xs)==len(gs)==6000
    forbidden={'preferred_action','acceptable_actions','latent','preference','authorization','stakes','reversibility','urgency'}
    assert all(not (forbidden & set(x.keys())) for x in xs)
def test_v2_group_split_has_no_counterfactual_leakage():
    sp=json.loads((ROOT/'grantshiftbench/v2/factorial_splits.json').read_text())
    tr,dv,te=map(set,(sp['train'],sp['dev'],sp['test']))
    assert not (tr&dv or tr&te or dv&te)
    assert len(tr|dv|te)==500
def test_v2_results_include_trivial_baselines_and_four_conditions():
    r=json.loads((ROOT/'artifacts/v2_factorial_results.json').read_text())
    for k in ['C0_state_only','C1_state_plus_preference','C2_state_plus_authorization','C3_full','always_ask','always_silent','always_act','always_suggest']:
        assert k in r
    assert r['always_ask']['question_burden']==1.0
    assert r['C3_full']['unauthorized_act_rate']==0.0
def test_croissant_and_empirical_status_exist():
    assert (ROOT/'grantshiftbench/croissant.json').exists()
    assert (ROOT/'docs/EMPIRICAL_STATUS.md').exists()
    assert (ROOT/'human_study/PROTOCOL.md').exists()
    assert (ROOT/'frontier_eval/export_prompts.py').exists()
