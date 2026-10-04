from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from grantshiftbench.loaders.jsonl import load_scenarios, select_split
from grantshift.policy.learned import LearnedPolicy
from grantshift.policy.frontier import AuthorizationFirstPolicy
from evaluation.significance import paired_accuracy_difference, mcnemar_exact


def compare(pa, pb, labels):
    return {
        "paired_bootstrap": paired_accuracy_difference(pa, pb, labels, n_boot=10000),
        "mcnemar_exact": mcnemar_exact(pa, pb, labels),
    }


def main():
    states,labels=load_scenarios(ROOT/'grantshiftbench/scenarios/v1.jsonl')
    tr_s,tr_l=select_split(states,labels,ROOT/'grantshiftbench/scenarios/splits.json','train')
    te_s,te_l=select_split(states,labels,ROOT/'grantshiftbench/scenarios/splits.json','test')
    g=LearnedPolicy(include_personalization=False).fit(tr_s,[x.preferred_action for x in tr_l])
    p=LearnedPolicy(include_personalization=True).fit(tr_s,[x.preferred_action for x in tr_l])
    gp=[g.decide(s).action for s in te_s]
    pp=[p.decide(s).action for s in te_s]

    fs,fl=load_scenarios(ROOT/'grantshiftbench/scenarios/frontier_v1.jsonl')
    base=[p.decide(s).action for s in fs]
    safe=AuthorizationFirstPolicy(p)
    sp=[safe.decide(s).action for s in fs]
    out={
        "main_generic_vs_personalized": compare(gp,pp,te_l),
        "frontier_unconstrained_vs_authorization_first": compare(base,sp,fl),
        "notes": "Paired tests are descriptive for this synthetic benchmark and do not establish real-user significance."
    }
    (ROOT/'artifacts/significance_results.json').write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))
if __name__=='__main__': main()
