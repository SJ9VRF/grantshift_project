from __future__ import annotations
import json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'artifacts/external_eval_power.json'

def n_for_two_prop(p1,p2,alpha=.05,power=.80):
    # Conservative independent-proportion normal approximation; paired designs usually need fewer items when predictions are correlated.
    z_alpha=1.959963984540054; z_beta=.8416212335729143
    pbar=(p1+p2)/2
    num=(z_alpha*math.sqrt(2*pbar*(1-pbar))+z_beta*math.sqrt(p1*(1-p1)+p2*(1-p2)))**2
    return math.ceil(num/((p1-p2)**2))

def main():
    scenarios=[]
    for p1,p2 in [(0.70,0.75),(0.75,0.80),(0.80,0.85),(0.85,0.90),(0.90,0.93),(0.90,0.95)]:
        scenarios.append({'baseline_exact':p1,'target_exact':p2,'absolute_delta':p2-p1,'approx_n_per_model_independent':n_for_two_prop(p1,p2)})
    out={'method':'two-sided alpha=.05, power=.80 normal approximation for two independent proportions; use as conservative planning guidance, not a substitute for paired/bootstrap analysis','scenarios':scenarios,'recommended_external_design':{'models_minimum':3,'runs_per_model_minimum':3,'primary_unit':'trajectory','report':['trajectory-cluster bootstrap CI','paired exact/McNemar where applicable','family-stratified error rates','run-to-run variance'],'prompt_pool_available':8892},'notes':['Pre-register the primary model comparison and metric before inspecting full results.','For repeated stochastic runs, estimate variance empirically and update power with a hierarchical or cluster-aware simulation.']}
    OUT.write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))
if __name__=='__main__':main()
