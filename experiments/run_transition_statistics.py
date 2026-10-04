from __future__ import annotations
import json, math
import numpy as np
from scipy.stats import binomtest
from collections import defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCES={
 'authorization_transitions':ROOT/'artifacts/authorization_transition_trials.jsonl',
 'scope_bound_authorization':ROOT/'artifacts/scope_bound_authorization_trials.jsonl',
}
OUT=ROOT/'artifacts/transition_statistics.json'

def load(path): return [json.loads(x) for x in path.read_text().splitlines() if x.strip()]

def mean(xs): return sum(xs)/len(xs) if xs else 0.0

def quantile(xs,q):
    xs=sorted(xs)
    if not xs: return 0.0
    pos=(len(xs)-1)*q; lo=int(math.floor(pos)); hi=int(math.ceil(pos))
    if lo==hi:return xs[lo]
    return xs[lo]*(hi-pos)+xs[hi]*(pos-lo)

def cluster_bootstrap(rows, metric, seed=1107, B=2000):
    byid=defaultdict(list)
    for r in rows: byid[r['trajectory_id']].append(r)
    ids=sorted(byid)
    nums=np.array([sum(float(x[metric]) for x in byid[i]) for i in ids],dtype=float)
    dens=np.array([len(byid[i]) for i in ids],dtype=float)
    rng=np.random.default_rng(seed)
    # Sample complete trajectories with replacement; vectorized for deterministic, fast CIs.
    idx=rng.integers(0,len(ids),size=(B,len(ids)))
    vals=nums[idx].sum(axis=1)/dens[idx].sum(axis=1)
    point=mean([float(x[metric]) for x in rows])
    return {'estimate':point,'ci95':[float(np.quantile(vals,.025)),float(np.quantile(vals,.975))],'bootstrap_clusters':len(ids),'bootstrap_replicates':B}

def exact_binom_two_sided(k,n):
    if n==0:return 1.0
    return float(binomtest(k,n,0.5,alternative='two-sided').pvalue)

def paired_mcnemar(rows, a, b):
    amap={(r['trajectory_id'],r['step']):bool(r['exact']) for r in rows if r['policy']==a}
    bmap={(r['trajectory_id'],r['step']):bool(r['exact']) for r in rows if r['policy']==b}
    keys=sorted(set(amap)&set(bmap)); a_only=sum(amap[k] and not bmap[k] for k in keys); b_only=sum(bmap[k] and not amap[k] for k in keys)
    n=a_only+b_only
    return {'policy_a':a,'policy_b':b,'paired_steps':len(keys),'a_correct_b_wrong':a_only,'b_correct_a_wrong':b_only,'discordant':n,'exact_two_sided_p':exact_binom_two_sided(min(a_only,b_only),n)}

def analyze(name,rows):
    policies=sorted({r['policy'] for r in rows}); metrics={}
    metric_names=['exact']
    if any('stale_authority_execution' in r for r in rows): metric_names += ['stale_authority_execution','premature_execution']
    if any('stale_scope_execution' in r for r in rows): metric_names += ['stale_scope_execution','premature_execution']
    for p in policies:
        rr=[r for r in rows if r['policy']==p]; metrics[p]={m:cluster_bootstrap(rr,m) for m in dict.fromkeys(metric_names)}
    if name=='authorization_transitions': pair=paired_mcnemar(rows,'static_initial_authority','authorization_state_machine')
    else: pair=paired_mcnemar(rows,'latest_authorization_label','scope_bound_state_machine')
    return {'policies':metrics,'paired_exact_comparison':pair}

def main():
    result={'method':'trajectory-cluster bootstrap 95% CIs; exact paired McNemar/sign test on step correctness','seed':1107,'benchmarks':{}}
    for name,path in SOURCES.items(): result['benchmarks'][name]=analyze(name,load(path))
    result['notes']=['Uncertainty quantifies sampling over synthetic trajectory cells only; it is not human/model population uncertainty.','Paired tests are mechanism checks and should not be interpreted as evidence of frontier-model superiority.']
    OUT.write_text(json.dumps(result,indent=2)+'\n'); print(json.dumps(result,indent=2))
if __name__=='__main__': main()
