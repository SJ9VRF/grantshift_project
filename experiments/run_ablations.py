from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from grantshiftbench.loaders.jsonl import load_scenarios,select_split
from grantshift.policy.learned import LearnedPolicy
from evaluation.metrics import evaluate

def main():
 s,l=load_scenarios(ROOT/"grantshiftbench/scenarios/v1.jsonl"); tr,tl=select_split(s,l,ROOT/"grantshiftbench/scenarios/splits.json","train"); te,el=select_split(s,l,ROOT/"grantshiftbench/scenarios/splits.json","test")
 cfgs={"full":{"core","risk","personalization","context"},"-risk":{"core","personalization","context"},"-personalization":{"core","risk","context"},"-context":{"core","risk","personalization"},"core_only":{"core"}}
 out={}
 for name,groups in cfgs.items():
  p=LearnedPolicy(include_personalization=("personalization" in groups),calibrated=False,feature_groups=groups).fit(tr,[x.preferred_action for x in tl])
  pr=[p.decide(x).action for x in te]; out[name]=evaluate(pr,el).__dict__
 (ROOT/"artifacts/ablation_results.json").write_text(json.dumps(out,indent=2)); print(json.dumps(out,indent=2))
if __name__=="__main__": main()
