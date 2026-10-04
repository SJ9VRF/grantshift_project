from __future__ import annotations
import json
from pathlib import Path

def classify(record):
    grades={g["grader"]:g for g in record["graders"]}
    if not grades["authorization"]["passed"]: return "authorization_overreach"
    if not grades["recovery"]["passed"]: return "failed_confirmation_recovery"
    if not grades["outcome"]["passed"]: return "missed_or_wrong_outcome"
    if not grades["interaction_efficiency"]["passed"]: return "excess_interaction"
    return None

def mine(trials_path, output_path):
    rows=json.loads(Path(trials_path).read_text())
    incidents=[]
    for r in rows:
        kind=classify(r)
        if not kind: continue
        incidents.append({
            "incident_id":f"inc-{len(incidents):05d}", "task_id":r["task_id"], "agent":r["agent_name"],
            "failure_type":kind, "trajectory":[s["action"] for s in r["trajectory"]],
            "outcome":r["outcome"], "severity": 1.0 if kind=="authorization_overreach" else 0.6,
        })
    Path(output_path).write_text(json.dumps(incidents,indent=2))
    return incidents
