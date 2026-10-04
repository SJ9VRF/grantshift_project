import json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def run(rel):
    return subprocess.run([sys.executable,str(ROOT/rel)],cwd=ROOT,check=True,capture_output=True,text=True)

def test_provenance_challenge_separates_latest_label():
    run('grantshiftbench/provenance/generate.py'); run('experiments/run_authorization_provenance_eval.py'); run('experiments/run_provenance_statistics.py')
    rows=[json.loads(x) for x in (ROOT/'grantshiftbench/provenance/authorization_provenance.jsonl').read_text().splitlines() if x.strip()]
    assert len(rows)==864
    d=json.loads((ROOT/'artifacts/authorization_provenance_eval.json').read_text())
    latest=d['policies']['latest_authorization_label']; prov=d['policies']['provenance_state_machine']
    assert latest['exact_rate']==2/3
    assert latest['invalid_provenance_execution_rate']==1/3
    assert prov['exact_rate']==1.0 and prov['invalid_provenance_execution_rate']==0.0
    st=json.loads((ROOT/'artifacts/authorization_provenance_statistics.json').read_text())
    assert st['paired_exact_comparison']['b_correct_a_wrong']==864
    assert st['paired_exact_comparison']['exact_two_sided_p'] < 1e-200

def test_unique_frontier_pool_and_integrity_audit():
    run('frontier_eval/export_transition_prompts.py'); run('frontier_eval/deduplicate_prompts.py'); run('scripts/audit_benchmark_integrity.py')
    full=sum(1 for x in (ROOT/'frontier_eval/transition_prompts.jsonl').read_text().splitlines() if x.strip())
    uniq=sum(1 for x in (ROOT/'frontier_eval/transition_prompts_unique.jsonl').read_text().splitlines() if x.strip())
    assert full==8892 and uniq==1602 and uniq < full
    d=json.loads((ROOT/'artifacts/benchmark_integrity_audit.json').read_text())
    assert d['ready'] is True and d['exact_prompt_duplicates_unique_pool']==0

def test_v12_docs_and_schema_exist():
    for rel in ['docs/ARTIFACT_CARD.md','docs/FRONTIER_EVAL_RUNBOOK.md','docs/INTERVIEW_TECHNICAL_NARRATIVE.md','frontier_eval/model_io_schema.json','artifacts/external_eval_power.json']:
        assert (ROOT/rel).exists(), rel
