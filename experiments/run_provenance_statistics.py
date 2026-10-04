from __future__ import annotations
import json, math, random
from collections import defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TR=ROOT/'artifacts/authorization_provenance_trials.jsonl'
OUT=ROOT/'artifacts/authorization_provenance_statistics.json'

def q(xs,p):
    xs=sorted(xs); x=(len(xs)-1)*p; lo=int(math.floor(x)); hi=int(math.ceil(x))
    return xs[lo] if lo==hi else xs[lo]*(hi-x)+xs[hi]*(x-lo)

def cluster_boot(rows, metric, B=2000, seed=12026):
    by=defaultdict(list)
    for r in rows: by[r['trajectory_id']].append(r)
    ids=list(by); rng=random.Random(seed); vals=[]
    for _ in range(B):
        sample=[rng.choice(ids) for _ in ids]; flat=[r for tid in sample for r in by[tid]]
        vals.append(sum(float(r[metric]) for r in flat)/len(flat))
    point=sum(float(r[metric]) for r in rows)/len(rows)
    return {'point':point,'ci95':[q(vals,.025),q(vals,.975)],'bootstrap_clusters':len(ids),'B':B}

def exact_binom_two_sided(k,n):
    # Exact two-sided sign/binomial test for discordant paired outcomes under p=.5.
    if n==0:return 1.0
    m=min(k,n-k)
    s=sum(math.comb(n,i) for i in range(m+1))/(2**n)
    return min(1.0,2*s)

def main():
    rows=[json.loads(x) for x in TR.read_text().splitlines() if x.strip()]
    byp=defaultdict(list)
    for r in rows:byp[r['policy']].append(r)
    out={'benchmark':'GrantShiftBench Authorization Provenance Challenge','policies':{},'paired_exact_comparison':{},'notes':['Trajectory-cluster bootstrap; synthetic instrument uncertainty only.']}
    for p,rs in byp.items():
        out['policies'][p]={'exact':cluster_boot(rs,'exact'),'invalid_provenance_execution':cluster_boot(rs,'invalid_provenance_execution')}
    a={(r['trajectory_id'],r['step']):r for r in byp['latest_authorization_label']}
    b={(r['trajectory_id'],r['step']):r for r in byp['provenance_state_machine']}
    a_correct_b_wrong=b_correct_a_wrong=0
    for key in a:
        ac=a[key]['exact']; bc=b[key]['exact']
        if ac and not bc:a_correct_b_wrong+=1
        if bc and not ac:b_correct_a_wrong+=1
    n=a_correct_b_wrong+b_correct_a_wrong
    out['paired_exact_comparison']={'a':'latest_authorization_label','b':'provenance_state_machine','a_correct_b_wrong':a_correct_b_wrong,'b_correct_a_wrong':b_correct_a_wrong,'discordant':n,'exact_two_sided_p':exact_binom_two_sided(a_correct_b_wrong,n)}
    OUT.write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))
if __name__=='__main__':main()
