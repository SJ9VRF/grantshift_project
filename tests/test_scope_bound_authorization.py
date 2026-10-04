import json, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def test_scope_bound_dataset_and_separation():
    subprocess.run([sys.executable,str(ROOT/'grantshiftbench/adversarial/generate.py')],check=True,cwd=ROOT,capture_output=True,text=True)
    subprocess.run([sys.executable,str(ROOT/'experiments/run_scope_bound_authorization_eval.py')],check=True,cwd=ROOT,capture_output=True,text=True)
    rows=[json.loads(x) for x in (ROOT/'grantshiftbench/adversarial/scope_bound_transitions.jsonl').read_text().splitlines() if x.strip()]
    assert len(rows)==1080
    result=json.loads((ROOT/'artifacts/scope_bound_authorization_eval.json').read_text())
    latest=result['policies']['latest_authorization_label']
    scoped=result['policies']['scope_bound_state_machine']
    assert latest['exact_rate'] < 0.90
    assert latest['stale_scope_execution_rate'] > 0.10
    assert scoped['exact_rate']==1.0
    assert scoped['stale_scope_execution_rate']==0.0

def test_transition_statistics_are_clustered_and_paired():
    subprocess.run([sys.executable,str(ROOT/'experiments/run_transition_statistics.py')],check=True,cwd=ROOT,capture_output=True,text=True)
    d=json.loads((ROOT/'artifacts/transition_statistics.json').read_text())
    s=d['benchmarks']['scope_bound_authorization']
    ci=s['policies']['latest_authorization_label']['exact']['ci95']
    assert ci[0] < 0.889 < ci[1]
    pair=s['paired_exact_comparison']
    assert pair['b_correct_a_wrong']==360
    assert pair['exact_two_sided_p'] < 1e-100

def test_frontier_transition_export_and_partial_scoring():
    subprocess.run([sys.executable,str(ROOT/'frontier_eval/export_transition_prompts.py')],check=True,cwd=ROOT,capture_output=True,text=True)
    prompts=[json.loads(x) for x in (ROOT/'frontier_eval/transition_prompts.jsonl').read_text().splitlines() if x.strip()]
    assert len(prompts)==8892
    # Partial prediction file is valid and scorer reports missing items rather than inventing outputs.
    with tempfile.TemporaryDirectory() as td:
        pred=Path(td)/'pred.jsonl'; out=Path(td)/'score.json'
        pred.write_text(json.dumps({'scenario_id':prompts[0]['scenario_id'],'action':'ask'})+'\n')
        subprocess.run([sys.executable,str(ROOT/'frontier_eval/score_transition_predictions.py'),str(pred),str(out)],check=True,cwd=ROOT,capture_output=True,text=True)
        d=json.loads(out.read_text())
        assert sum(x['n_scored'] for x in d['suites'].values())==1
        assert sum(x['n_missing'] for x in d['suites'].values())==8891

def test_v11_research_docs_exist():
    for rel in ['docs/CLAIM_ABLATION_MATRIX.md','docs/EXTERNAL_BENCHMARK_ADAPTER.md','docs/HIRING_MANAGER_BRIEF.md','reports/reviewer_failure_analysis.md']:
        assert (ROOT/rel).exists(), rel
