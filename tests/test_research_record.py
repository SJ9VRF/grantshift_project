from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]

def test_research_record_files_exist():
    for rel in ['docs/RESEARCH_DECISION_LOG.md','docs/EXPERIMENT_REGISTRY.md','docs/OPENAI_ANTHROPIC_REVIEW.md','configs/research_claims.yaml']:
        assert (ROOT/rel).exists(), rel

def test_external_claims_are_unverified():
    data=yaml.safe_load((ROOT/'configs/research_claims.yaml').read_text())
    by_id={x['id']:x for x in data['claims']}
    assert by_id['c4']['status']=='unverified_external'
    assert by_id['c5']['status']=='unverified_human'
    assert by_id['c4']['evidence']==[] and by_id['c5']['evidence']==[]

def test_decision_log_records_known_failures():
    t=(ROOT/'docs/RESEARCH_DECISION_LOG.md').read_text().lower()
    for phrase in ['oracle-visible','paraphrase','trajectories','revocation','external evidence']:
        assert phrase in t
