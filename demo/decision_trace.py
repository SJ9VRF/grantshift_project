from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from grantshiftbench.loaders.jsonl import load_scenarios
from grantshift.policy.heuristic import decide

def main():
 states,_=load_scenarios(ROOT/"grantshiftbench/scenarios/v1.jsonl")
 for s in states[:5]:
  d=decide(s)
  print("\n",s.scenario_id,s.domain,"=>",d.action.value)
  print(f"risk={d.risk:.2f} confidence={d.confidence:.2f} utility={d.utility:.2f}")
  for r in d.reasons: print(" -",r)
if __name__=="__main__": main()
