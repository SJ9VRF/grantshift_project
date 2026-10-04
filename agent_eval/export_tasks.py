from __future__ import annotations
import json
from dataclasses import asdict
from pathlib import Path
from .suite import build_suite

def serialize(t):
    return {"task_id":t.task_id,"domain":t.state.domain,"goal":t.state.goal,"authorization":t.authorization,
            "recoverable":t.recoverable,"max_turns":t.max_turns,"tags":t.tags}

def main():
    root=Path(__file__).resolve().parent
    tasks=build_suite()
    capability=[t for t in tasks if t.authorization=="ask_required" or not t.recoverable]
    regression=[t for t in tasks if t.authorization in {"prohibited","preauthorized"} and t.recoverable]
    (root/'capability_tasks.jsonl').write_text('\n'.join(json.dumps(serialize(t)) for t in capability)+'\n')
    (root/'regression_tasks.jsonl').write_text('\n'.join(json.dumps(serialize(t)) for t in regression)+'\n')
    print(json.dumps({"capability":len(capability),"regression":len(regression)}))
if __name__=='__main__': main()
