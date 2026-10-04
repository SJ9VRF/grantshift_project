from pathlib import Path
import shutil, zipfile, re, json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'submission'
STAGE=OUT/'anonymous_source'
if STAGE.exists(): shutil.rmtree(STAGE)
STAGE.mkdir(parents=True)
include=['paper','grantshiftbench/v2','evaluation','agent_eval','posttraining','experiments/run_v2_factorial.py','experiments/run_v2_surface_generalization.py','experiments/run_v2_robustness_suite.py','experiments/run_utility_sensitivity.py','experiments/run_long_horizon_v2.py','experiments/run_agent_trajectory_eval.py','experiments/run_cross_environment_eval.py','experiments/run_authorization_transition_eval.py','experiments/run_scope_bound_authorization_eval.py','experiments/run_transition_statistics.py','experiments/run_authorization_provenance_eval.py','experiments/run_provenance_statistics.py','experiments/run_external_power_analysis.py','grantshiftbench/transitions','grantshiftbench/adversarial','grantshiftbench/provenance','grantshiftbench/capability_ledger','experiments/run_capability_ledger_eval.py','experiments/run_capability_ledger_statistics.py','experiments/run_capability_mutation_eval.py','frontier_eval','human_study','configs/submission_experiments.yaml','configs/claim_evidence_registry.json','evaluation/grader_rubric_cases.json','evaluation/run_grader_rubric_regression.py','scripts/validate_claim_evidence.py','scripts/build_paper_figures.py','scripts/build_agent_eval_figures.py','scripts/reproduce_submission.sh','references.bib','requirements-lock.txt','LICENSE']
for rel in include:
    src=ROOT/rel
    dst=STAGE/rel
    if src.is_dir(): shutil.copytree(src,dst,ignore=shutil.ignore_patterns('__pycache__','*.pyc','*.pdf','*.zip','*.whl'))
    elif src.exists(): dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,dst)
# Remove public author from any copied text source. Anonymous paper wrapper already sets Anonymous Authors.
for p in STAGE.rglob('*'):
    if p.is_file() and p.suffix.lower() in {'.md','.tex','.bib','.json','.yaml','.yml','.py','.sh','.txt'}:
        try: s=p.read_text()
        except UnicodeDecodeError: continue
        s=s.replace('Aura Yavary','Anonymous Author')
        p.write_text(s)
# Copy anonymous PDF only.
shutil.copy2(ROOT/'paper/grantshift-paper-anonymous-v1.4.0.pdf',STAGE/'paper/grantshift-paper-anonymous-v1.4.0.pdf')
zip_path=OUT/'grantshift-anonymous-submission-v1.4.0.zip'
if zip_path.exists(): zip_path.unlink()
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(STAGE.rglob('*')):
        if p.is_file(): z.write(p,p.relative_to(STAGE))
# audit forbidden identifiers
hits=[]
for p in STAGE.rglob('*'):
    if p.is_file() and p.suffix.lower() in {'.md','.tex','.bib','.json','.yaml','.yml','.py','.sh','.txt'}:
        try:
            if 'Aura Yavary' in p.read_text(): hits.append(str(p.relative_to(STAGE)))
        except UnicodeDecodeError: pass
# Also audit filenames and extracted PDF text so stale public artifacts cannot hide in the anonymous zip.
name_hits=[str(p.relative_to(STAGE)) for p in STAGE.rglob('*') if p.is_file() and ('Aura' in p.name or 'Yavary' in p.name)]
pdf_hits=[]
for pdf in STAGE.rglob('*.pdf'):
    try:
        import subprocess
        txt=subprocess.run(['pdftotext',str(pdf),'-'],capture_output=True,text=True,check=False).stdout
        if 'Aura Yavary' in txt: pdf_hits.append(str(pdf.relative_to(STAGE)))
    except Exception:
        pass
report={'zip':str(zip_path),'author_string_hits':hits,'filename_identifier_hits':name_hits,'pdf_text_identifier_hits':pdf_hits,'ready':not hits and not name_hits and not pdf_hits}
(OUT/'anonymous_submission_audit.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
