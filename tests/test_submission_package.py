from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]

def test_v2_input_has_no_structured_latent_fields():
    row=json.loads((ROOT/'grantshiftbench/v2/factorial_inputs.jsonl').read_text().splitlines()[0])
    forbidden={'preference','authorization','stakes','reversibility','urgency','preferred_action','acceptable_actions'}
    assert not (forbidden & set(row))

def test_group_split_is_disjoint():
    s=json.loads((ROOT/'grantshiftbench/v2/factorial_splits.json').read_text())
    a,b,c=map(set,(s['train'],s['dev'],s['test']))
    assert not a&b and not a&c and not b&c

def test_paraphrase_stress_artifact_exists():
    p=ROOT/'artifacts/v2_surface_generalization.json'; assert p.exists()
    d=json.loads(p.read_text()); assert d['metadata']['n']==900

def test_submission_sources_exist():
    required=['paper/main.tex','paper/main_anonymous.tex','paper/paper_body.tex','configs/submission_experiments.yaml','docs/COMPUTE_DISCLOSURE.md','human_study/PROTOCOL.md','frontier_eval/README.md']
    for rel in required: assert (ROOT/rel).exists(), rel

def test_external_results_not_fabricated():
    status=(ROOT/'docs/EMPIRICAL_STATUS.md').read_text().lower()
    assert 'not completed and not claimed' in status and 'human gold labels' in status

def test_anonymous_bundle_contains_only_anonymous_pdf():
    import zipfile
    zpath=ROOT/'submission/grantshift-anonymous-submission-v1.7.0.zip'
    if not zpath.exists():
        import pytest; pytest.skip('release-only anonymous bundle not present in source checkout')
    with zipfile.ZipFile(zpath) as z:
        names=z.namelist()
    pdfs=[n for n in names if n.lower().endswith('.pdf')]
    assert pdfs==['paper/grantshift-paper-anonymous-v1.7.0.pdf']
    assert not any('aura' in n.lower() or 'yavary' in n.lower() or '1.0.0' in n for n in names)
