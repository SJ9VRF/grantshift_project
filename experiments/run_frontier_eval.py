from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from grantshiftbench.loaders.jsonl import load_scenarios, select_split
from grantshift.policy.learned import LearnedPolicy
from grantshift.policy.frontier import AuthorizationFirstPolicy
from grantshift.policy.constrained import ConstrainedInterventionPolicy
from evaluation.metrics import evaluate
from evaluation.frontier_metrics import intervention_frontier_metrics
from evaluation.counterfactual import authorization_counterfactual_metrics


def main():
    train_states,train_labels=load_scenarios(ROOT/'grantshiftbench/scenarios/v1.jsonl')
    tr_s,tr_l=select_split(train_states,train_labels,ROOT/'grantshiftbench/scenarios/splits.json','train')
    fs,fl=load_scenarios(ROOT/'grantshiftbench/scenarios/frontier_v1.jsonl')
    generic=LearnedPolicy(include_personalization=False).fit(tr_s,[x.preferred_action for x in tr_l])
    personal=LearnedPolicy(include_personalization=True).fit(tr_s,[x.preferred_action for x in tr_l])
    generic_frontier=AuthorizationFirstPolicy(generic)
    frontier=AuthorizationFirstPolicy(personal)
    constrained_generic=ConstrainedInterventionPolicy(generic)
    constrained_personal=ConstrainedInterventionPolicy(personal)
    result={}
    for name,model in [('generic',generic),('generic_authorization_first',generic_frontier),('generic_constrained_ranker',constrained_generic),('personalized_unconstrained',personal),('grantshift_authorization_first',frontier),('grantshift_constrained_ranker',constrained_personal)]:
        preds=[model.decide(s).action for s in fs]
        result[name]={**evaluate(preds,fl).__dict__,**intervention_frontier_metrics(fs,preds,fl),**authorization_counterfactual_metrics(fs,preds,fl)}
    result['metadata']={'benchmark':'GrantShiftBench Frontier Set','n':len(fs),'matched_groups':len(fs)//4,'changed_variable':'authorization','synthetic_labels':True}
    (ROOT/'artifacts/frontier_eval.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))
if __name__=='__main__': main()
