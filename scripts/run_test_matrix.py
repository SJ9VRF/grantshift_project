from __future__ import annotations
import json, subprocess, sys, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
files=sorted(str(x.relative_to(ROOT)) for x in (ROOT/'tests').glob('test_*.py'))
chunks=[files[i:i+8] for i in range(0,len(files),8)]
rows=[]; total_passed=0; ok=True
for i,chunk in enumerate(chunks):
    t=time.time(); r=subprocess.run([sys.executable,'-m','pytest','-q',*chunk],cwd=ROOT,capture_output=True,text=True); elapsed=time.time()-t
    line=(r.stdout.strip().splitlines()[-1] if r.stdout.strip() else '')
    passed=0
    import re
    m=re.search(r'(\d+) passed',line)
    if m: passed=int(m.group(1))
    total_passed+=passed; ok &= r.returncode==0
    rows.append({'chunk':i,'files':chunk,'returncode':r.returncode,'passed':passed,'elapsed_seconds':round(elapsed,3),'summary':line,'stderr':r.stderr.strip()[-1000:]})
report={'test_files':len(files),'chunks':rows,'total_passed':total_passed,'all_passed':bool(ok)}
(ROOT/'artifacts/test_matrix.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
raise SystemExit(0 if ok else 1)
