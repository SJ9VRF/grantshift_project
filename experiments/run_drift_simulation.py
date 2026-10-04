from pathlib import Path
import json,sys,copy
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from grantshift.types import Action,AutonomyProfile,AgentState
from grantshift.policy.heuristic import decide

def main():
 base=AgentState(scenario_id="drift",domain="productivity",goal="submit application",urgency=.72,intent_confidence=.95,execution_confidence=.95,stakes=.35,reversibility=.95,expected_benefit=.8,time_sensitivity=.85)
 pre=AutonomyProfile(domain_preferences={"productivity":Action.REMIND}, interruption_tolerance=.8, default_action=Action.SUGGEST)
 post=AutonomyProfile(domain_preferences={"productivity":Action.DO_NOTHING}, interruption_tolerance=.1, default_action=Action.DO_NOTHING)
 hist=[]
 for i in range(30):
  true_profile=pre if i<15 else post
  true_target=Action.REMIND if i<15 else Action.DO_NOTHING
  frozen=copy.deepcopy(base); frozen.user_profile=pre
  adaptive=copy.deepcopy(base); adaptive.user_profile=true_profile
  hist.append({"turn":i+1,"true_target":true_target.value,"frozen":decide(frozen).action.value,"adaptive":decide(adaptive).action.value,"post_drift":i>=15})
 def acc(key,part): return sum(x[key]==x["true_target"] for x in part)/len(part)
 out={"frozen_pre":acc("frozen",hist[:15]),"frozen_post":acc("frozen",hist[15:]),"adaptive_pre":acc("adaptive",hist[:15]),"adaptive_post":acc("adaptive",hist[15:]),"history":hist}
 (ROOT/"artifacts/drift_results.json").write_text(json.dumps(out,indent=2));print(json.dumps({k:v for k,v in out.items() if k!="history"},indent=2))
if __name__=="__main__":main()
