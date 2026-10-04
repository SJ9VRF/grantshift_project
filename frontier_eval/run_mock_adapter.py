"""Offline adapter smoke test. It never calls an external model and must not be reported as frontier-model evidence."""
from __future__ import annotations
import argparse, json, time
from pathlib import Path

def choose(prompt:str):
    p=prompt.lower()
    if 'revoked' in p or 'denies' in p or 'denied' in p or 'expires' in p or 'expired' in p: return 'do_nothing'
    if 'requires confirmation' in p or 'needs its own confirmation' in p or 'not an authorized principal' in p or 'old grant' in p or 'old n-a1' in p: return 'ask'
    if 'grant' in p or 'authorized this specific action' in p or 'valid confirmation' in p: return 'act'
    return 'ask'

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--prompts',default='frontier_eval/transition_prompts.jsonl'); ap.add_argument('--out',default='artifacts/mock_frontier_predictions.jsonl'); ap.add_argument('--limit',type=int,default=25); args=ap.parse_args()
    rows=[]
    for line in Path(args.prompts).read_text().splitlines()[:args.limit]:
        r=json.loads(line); t=time.perf_counter(); action=choose(r['prompt']); latency=(time.perf_counter()-t)*1000
        rows.append({'scenario_id':r['scenario_id'],'action':action,'model':'offline-rule-smoke-test','provider':'local','run_id':'mock-smoke-001','temperature':None,'seed':None,'raw_response':None,'latency_ms':latency,'input_tokens':None,'output_tokens':None})
    Path(args.out).write_text('\n'.join(json.dumps(r) for r in rows)+'\n'); print(json.dumps({'n':len(rows),'output':args.out,'evidence_status':'adapter smoke test only'},indent=2))
if __name__=='__main__': main()
