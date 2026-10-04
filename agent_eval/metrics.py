from __future__ import annotations
from collections import defaultdict
import math

def pass_at_k(p: float, k: int) -> float:
    return 1.0 - (1.0 - p) ** k

def pass_pow_k(p: float, k: int) -> float:
    return p ** k

def summarize(records, k_values=(1,3,5)):
    grouped = defaultdict(list)
    for r in records: grouped[r.agent_name].append(r)
    out = {}
    for agent, rows in grouped.items():
        p = sum(r.passed for r in rows) / len(rows)
        auth = [next(g for g in r.graders if g.grader == "authorization") for r in rows]
        interaction = [next(g for g in r.graders if g.grader == "interaction_efficiency") for r in rows]
        recovery_rows = [next(g for g in r.graders if g.grader == "recovery") for r in rows if not next(g for g in r.graders if g.grader == "recovery").details.get("not_applicable")]
        tracking_rows = [next(g for g in r.graders if g.grader == "state_tracking") for r in rows if not next(g for g in r.graders if g.grader == "state_tracking").details.get("not_applicable")]
        latencies = [s.latency_ms for r in rows for s in r.trajectory]
        turns = [len(r.trajectory) for r in rows]
        out[agent] = {
            "n_trials": len(rows), "pass_rate": p,
            "authorization_pass_rate": sum(g.passed for g in auth)/len(auth),
            "mean_interaction_score": sum(g.score for g in interaction)/len(interaction),
            "recovery_rate": (sum(g.passed for g in recovery_rows)/len(recovery_rows)) if recovery_rows else None,
            "state_tracking_rate": (sum(g.passed for g in tracking_rows)/len(tracking_rows)) if tracking_rows else None,
            "mean_turns": sum(turns)/len(turns),
            "mean_policy_latency_ms": sum(latencies)/len(latencies),
            "pass_at_k": {str(k): pass_at_k(p,k) for k in k_values},
            "pass_pow_k": {str(k): pass_pow_k(p,k) for k in k_values},
        }
    return out
