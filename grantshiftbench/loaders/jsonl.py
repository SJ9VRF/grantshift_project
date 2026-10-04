from __future__ import annotations
import json
from pathlib import Path
from grantshift.types import Action, AgentState, AutonomyProfile, ScenarioLabel

def load_scenarios(path):
    states=[]; labels=[]
    with open(path) as f:
        for line in f:
            if not line.strip(): continue
            raw=json.loads(line)
            r=raw.get("state", raw)
            p=r.get("user_profile",{})
            profile=AutonomyProfile(
                domain_preferences={k:Action(v) for k,v in p.get("domain_preferences",{}).items()},
                interruption_tolerance=float(p.get("interruption_tolerance",.5)),
                default_action=Action(p.get("default_action","ask")),
            )
            state=AgentState(
                scenario_id=r["scenario_id"],domain=r["domain"],goal=r["goal"],
                urgency=float(r["urgency"]),intent_confidence=float(r["intent_confidence"]),execution_confidence=float(r["execution_confidence"]),
                stakes=float(r["stakes"]),reversibility=float(r["reversibility"]),expected_benefit=float(r["expected_benefit"]),
                financial_cost=float(r.get("financial_cost",0)),social_cost=float(r.get("social_cost",0)),privacy_risk=float(r.get("privacy_risk",0)),
                safety_risk=float(r.get("safety_risk",0)),time_sensitivity=float(r.get("time_sensitivity",0)),user_profile=profile,metadata=r.get("metadata",{})
            )
            l=raw["label"]
            label=ScenarioLabel(Action(l["preferred_action"]),[Action(x) for x in l["acceptable_actions"]],[Action(x) for x in l.get("bad_actions",[])],float(l["severity_of_wrong_action"]))
            states.append(state); labels.append(label)
    return states,labels

def select_split(states, labels, splits_path, split):
    ids=set(json.loads(Path(splits_path).read_text())[split])
    pairs=[(s,l) for s,l in zip(states,labels) if s.scenario_id in ids]
    return [x[0] for x in pairs],[x[1] for x in pairs]

# Backward-compatible alias for v0 tests.
def load_jsonl(path):
    return load_scenarios(path)
