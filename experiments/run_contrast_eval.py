from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from grantshiftbench.loaders.jsonl import load_scenarios,select_split
from grantshift.policy.learned import LearnedPolicy
from evaluation.metrics import evaluate

def main():
 s,l=load_scenarios(ROOT/"grantshiftbench/scenarios/v1.jsonl"); tr,tl=select_split(s,l,ROOT/"grantshiftbench/scenarios/splits.json","train")
 cs,cl=load_scenarios(ROOT/"grantshiftbench/scenarios/contrast_v1.jsonl")
 # Every base state appears under multiple user profiles. Train on first half of base states, test on held-out states.
 cut=len(cs)//2; ctrain,cltrain=cs[:cut],cl[:cut]; ctest,cltest=cs[cut:],cl[cut:]
 out={}
 for name,pers in [("generic",False),("personalized",True)]:
  train_s=tr+ctrain; train_l=tl+cltrain
  p=LearnedPolicy(include_personalization=pers,calibrated=False).fit(train_s,[x.preferred_action for x in train_l]); pr=[p.decide(x).action for x in ctest]; out[name]=evaluate(pr,cltest).__dict__
 (ROOT/"artifacts/contrast_results.json").write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
if __name__=="__main__":main()
