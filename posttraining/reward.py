from __future__ import annotations

def trajectory_reward(record: dict) -> float:
    grades={g["grader"]:g for g in record["graders"]}
    auth=grades["authorization"]["score"]
    outcome=grades["outcome"]["score"]
    recovery=grades["recovery"]["score"]
    efficiency=grades["interaction_efficiency"]["score"]
    turns=len(record["trajectory"])
    # Lexicographic priorities are approximated with a large safety penalty.
    return 2.0*outcome + 0.75*recovery + 0.5*efficiency + 1.5*auth - 4.0*(1.0-auth) - 0.03*max(0,turns-1)
