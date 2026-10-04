from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]

def test_evidence_graph_has_no_orphans_or_missing_files():
    d=json.loads((ROOT/'evidence/EVIDENCE_GRAPH.json').read_text())
    assert d['integrity']['claims_without_experiment_links']==[]
    assert d['integrity']['evidence_files_missing']==[]
    assert len(d['claims'])==11

def test_release_consistency_gate_ready():
    d=json.loads((ROOT/'artifacts/release_consistency_audit.json').read_text())
    assert d['ready'] is True
    assert all(x['pass'] for x in d['checks'])

def test_core_reproduction_report_ready():
    d=json.loads((ROOT/'artifacts/core_reproduction_report.json').read_text())
    assert d['ready'] is True
    assert len(d['commands'])==5
    assert all(x['returncode']==0 for x in d['commands'])

def test_reviewer_red_team_preserves_evidence_boundary():
    t=(ROOT/'evidence/REVIEWER_RED_TEAM.md').read_text().lower()
    for phrase in ['does not establish model competence','human labels','production-safety','sota claims']:
        assert phrase in t
