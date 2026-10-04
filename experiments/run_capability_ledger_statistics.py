from __future__ import annotations
import json, math, random
from collections import defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TRIALS=ROOT/'artifacts/capability_ledger_trials.jsonl'; OUT=ROOT/'artifacts/capability_ledger_statistics.json'

def load(): return [json.loads(x) for x in TRIALS.read_text().splitlines() if x.strip()]
def ci(vals,seed=13027,B=4000):
    rng=random.Random(seed); n=len(vals); means=[]
    for _ in range(B): means.append(sum(vals[rng.randrange(n)] for _ in range(n))/n)
    means.sort(); return [means[int(.025*B)],means[int(.975*B)-1]]
def main():
    rows=load(); by=defaultdict(list)
    for r in rows: by[r['policy']].append(r)
    out={'benchmark':'GrantShiftBench Capability Ledger Challenge','unit':'trajectory-cluster bootstrap','policies':{}}
    for pol,rs in sorted(by.items()):
        tr=defaultdict(list)
        for r in rs: tr[r['trajectory_id']].append(r)
        exact=[sum(x['exact'] for x in xs)/len(xs) for xs in tr.values()]
        bad=[sum(x['invalid_capability_execution'] for x in xs)/len(xs) for xs in tr.values()]
        out['policies'][pol]={'n_trajectories':len(tr),'exact_rate':sum(exact)/len(exact),'exact_95ci':ci(exact),
                              'invalid_execution_rate':sum(bad)/len(bad),'invalid_execution_95ci':ci(bad,13028)}
    # paired discordance against capability ledger
    gold={(r['trajectory_id'],r['step']):r['exact'] for r in by['capability_ledger']}
    out['paired_vs_capability_ledger']={}
    for pol in ['latest_authorization_label','flat_provenance']:
        other={(r['trajectory_id'],r['step']):r['exact'] for r in by[pol]}
        b=sum(gold[k] and not other[k] for k in gold); c=sum(other[k] and not gold[k] for k in gold)
        # exact two-sided sign/binomial p for discordant pairs; here c expected zero but general form retained.
        n=b+c
        if n==0: p=1.0
        else:
            tail=sum(math.comb(n,i) for i in range(0,min(b,c)+1))/(2**n)
            p=min(1.0,2*tail)
        out['paired_vs_capability_ledger'][pol]={'ledger_better':b,'other_better':c,'discordant_steps':n,'two_sided_exact_p':p}
    OUT.write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))
if __name__=='__main__': main()
