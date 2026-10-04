from __future__ import annotations
import json
from pathlib import Path

CORRECTION={
 "authorization_overreach":"Prefer a non-mutating action that respects the active authorization boundary.",
 "failed_confirmation_recovery":"Ask once, incorporate the user's answer, then complete the now-authorized action.",
 "missed_or_wrong_outcome":"Choose the least intrusive action that still achieves the authorized outcome.",
 "excess_interaction":"Avoid redundant questions or interventions once sufficient information is available.",
}

def build(incidents_path, output_path):
    incidents=json.loads(Path(incidents_path).read_text())
    pairs=[]
    for x in incidents:
        pairs.append({"id":x["incident_id"],"prompt":f"Task {x['task_id']} failed as {x['failure_type']}.",
                      "rejected":" -> ".join(x["trajectory"]),"chosen":CORRECTION[x["failure_type"]],
                      "weight":x["severity"]})
    Path(output_path).write_text("\n".join(json.dumps(p) for p in pairs)+("\n" if pairs else ""))
    return pairs
