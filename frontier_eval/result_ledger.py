from __future__ import annotations
import argparse, hashlib, json
from collections import defaultdict
from pathlib import Path

ALLOWED={"act","ask","suggest","remind","wait","defer","do_nothing"}
REQ={"scenario_id","action","model","provider","run_id"}

def load(path: Path):
    rows=[]
    for i,line in enumerate(path.read_text().splitlines(),1):
        if not line.strip(): continue
        r=json.loads(line); miss=REQ-r.keys()
        if miss: raise ValueError(f"line {i}: missing {sorted(miss)}")
        if r['action'] not in ALLOWED: raise ValueError(f"line {i}: invalid action {r['action']}")
        rows.append(r)
    return rows

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('predictions',nargs='+'); ap.add_argument('--out',default='artifacts/frontier_result_ledger.json'); args=ap.parse_args()
    runs=defaultdict(lambda:{'n':0,'models':set(),'providers':set(),'files':set(),'scenario_ids':set(),'duplicate_scenarios':0,'latency_ms':[],'input_tokens':0,'output_tokens':0})
    for fn in args.predictions:
        p=Path(fn); rows=load(p); sha=hashlib.sha256(p.read_bytes()).hexdigest()
        for r in rows:
            x=runs[r['run_id']]; x['n']+=1; x['models'].add(r['model']); x['providers'].add(r['provider']); x['files'].add(str(p));
            if r['scenario_id'] in x['scenario_ids']: x['duplicate_scenarios']+=1
            x['scenario_ids'].add(r['scenario_id'])
            if r.get('latency_ms') is not None: x['latency_ms'].append(float(r['latency_ms']))
            x['input_tokens'] += int(r.get('input_tokens') or 0); x['output_tokens'] += int(r.get('output_tokens') or 0)
        runs[r['run_id']]['sha256']=sha if len(args.predictions)==1 else None
    out={'schema_version':'1.0','runs':{}}
    for rid,x in sorted(runs.items()):
        out['runs'][rid]={
            'n_predictions':x['n'],'n_unique_scenarios':len(x['scenario_ids']),'duplicate_scenarios':x['duplicate_scenarios'],
            'models':sorted(x['models']),'providers':sorted(x['providers']),'files':sorted(x['files']),
            'mean_latency_ms':sum(x['latency_ms'])/len(x['latency_ms']) if x['latency_ms'] else None,
            'input_tokens':x['input_tokens'],'output_tokens':x['output_tokens'],'sha256':x.get('sha256')
        }
    Path(args.out).write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))
if __name__=='__main__': main()
