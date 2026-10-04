from pathlib import Path
import subprocess,sys,json,hashlib,platform,time,os
ROOT=Path(__file__).resolve().parents[1]
commands=[
 [sys.executable,'experiments/run_capability_ledger_eval.py'],
 [sys.executable,'experiments/run_capability_mutation_eval.py'],
 [sys.executable,'scripts/build_evidence_graph.py'],
 [sys.executable,'scripts/validate_claim_evidence.py'],
 [sys.executable,'scripts/audit_release_consistency.py'],
]
runs=[]
for cmd in commands:
    t=time.time(); p=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True)
    runs.append({'command':' '.join(cmd),'returncode':p.returncode,'seconds':round(time.time()-t,3),'stdout_tail':p.stdout[-1200:],'stderr_tail':p.stderr[-1200:]})
    if p.returncode: break
tracked=['artifacts/capability_ledger_eval.json','artifacts/capability_mutation_eval.json','evidence/EVIDENCE_GRAPH.json','artifacts/claim_evidence_audit.json','artifacts/release_consistency_audit.json']
hashes={}
for rel in tracked:
    p=ROOT/rel
    if p.exists(): hashes[rel]=hashlib.sha256(p.read_bytes()).hexdigest()
report={'version':'1.7.0','python':sys.version.split()[0],'platform':platform.platform(),'commands':runs,'sha256':hashes,'ready':len(runs)==len(commands) and all(r['returncode']==0 for r in runs)}
(ROOT/'artifacts/core_reproduction_report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
raise SystemExit(0 if report['ready'] else 1)
