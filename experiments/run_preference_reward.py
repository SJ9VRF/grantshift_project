from pathlib import Path
import json,sys,random
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from grantshiftbench.loaders.jsonl import load_scenarios,select_split
from grantshift.reward.pairwise import PairwiseRewardModel
from grantshift.types import Action
from evaluation.metrics import evaluate

def main():
 s,l=load_scenarios(ROOT/"grantshiftbench/scenarios/v1.jsonl"); tr,tl=select_split(s,l,ROOT/"grantshiftbench/scenarios/splits.json","train"); te,el=select_split(s,l,ROOT/"grantshiftbench/scenarios/splits.json","test")
 rng=random.Random(1); pairs=[]
 for st,lab in zip(tr,tl):
  rejects=[a for a in Action if a!=lab.preferred_action]
  for r in rng.sample(rejects,min(2,len(rejects))): pairs.append((st,lab.preferred_action,r))
 rm=PairwiseRewardModel().fit(pairs); preds=[rm.decide(x) for x in te]; res=evaluate(preds,el).__dict__
 (ROOT/"artifacts/reward_model_results.json").write_text(json.dumps(res,indent=2)); print(json.dumps(res,indent=2))
if __name__=="__main__": main()
