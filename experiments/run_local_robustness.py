from pathlib import Path
import copy, json, random, sys
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from grantshiftbench.loaders.jsonl import load_scenarios, select_split
from grantshift.policy.learned import LearnedPolicy
from grantshift.types import Action

FIELDS=['urgency','intent_confidence','execution_confidence','stakes','reversibility','expected_benefit','financial_cost','social_cost','privacy_risk','safety_risk','time_sensitivity']

def perturb(s, rng, eps):
    q=copy.deepcopy(s)
    for f in FIELDS:
        v=getattr(q,f)
        setattr(q,f,max(0.0,min(1.0,float(v)+rng.uniform(-eps,eps))))
    q.scenario_id=s.scenario_id+'-jitter'
    return q

def batch_predict(model, states):
    X=pd.DataFrame(model._records(states))
    return [Action(x) for x in model.model.predict(X)]

def main():
    states,labels=load_scenarios(ROOT/'grantshiftbench/scenarios/v1.jsonl')
    tr_s,tr_l=select_split(states,labels,ROOT/'grantshiftbench/scenarios/splits.json','train')
    te_s,_=select_split(states,labels,ROOT/'grantshiftbench/scenarios/splits.json','test')
    model=LearnedPolicy(include_personalization=True).fit(tr_s,[x.preferred_action for x in tr_l])
    base=batch_predict(model,te_s)
    out={}
    for eps in [0.005,0.01,0.02,0.05]:
        stable=0; total=0
        for rep in range(10):
            rng=random.Random(1000+rep)
            pert=[perturb(s,rng,eps) for s in te_s]
            pred=batch_predict(model,pert)
            stable += sum(a==b for a,b in zip(base,pred))
            total += len(base)
        out[str(eps)]={"action_stability":stable/total,"comparisons":total}
    out['notes']='Local numeric-jitter stability is a sensitivity diagnostic, not a correctness metric.'
    (ROOT/'artifacts/local_robustness.json').write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))
if __name__=='__main__': main()
