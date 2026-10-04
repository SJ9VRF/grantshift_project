from __future__ import annotations
import json
from collections import Counter, defaultdict
from pathlib import Path

def prioritize(incidents_path, output_path):
    rows=json.loads(Path(incidents_path).read_text())
    freq=Counter(x["failure_type"] for x in rows)
    groups=defaultdict(list)
    for x in rows: groups[x["failure_type"]].append(x)
    ranking=[]
    for kind, xs in groups.items():
        severity=sum(x["severity"] for x in xs)/len(xs)
        frequency=freq[kind]/max(1,len(rows))
        priority=0.65*severity+0.35*frequency
        ranking.append({"failure_type":kind,"count":len(xs),"mean_severity":severity,"frequency":frequency,"priority":priority})
    ranking.sort(key=lambda x:x["priority"], reverse=True)
    Path(output_path).write_text(json.dumps(ranking,indent=2))
    return ranking
