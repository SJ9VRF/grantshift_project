from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from grantshift.policy.learned import LearnedPolicy
from grantshiftbench.loaders.jsonl import load_scenarios, select_split

ROOT = Path(__file__).resolve().parents[1]


def main():
    states, labels = load_scenarios(ROOT / "grantshiftbench/scenarios/v1.jsonl")
    tr_s, tr_l = select_split(states, labels, ROOT / "grantshiftbench/scenarios/splits.json", "train")
    dv_s, dv_l = select_split(states, labels, ROOT / "grantshiftbench/scenarios/splits.json", "dev")
    te_s, te_l = select_split(states, labels, ROOT / "grantshiftbench/scenarios/splits.json", "test")
    policy = LearnedPolicy(include_personalization=True).fit(tr_s, [l.preferred_action for l in tr_l])
    policy.calibrate(dv_s, [l.preferred_action for l in dv_l])

    rows = []
    decisions = [policy.decide(s) for s in te_s]
    for threshold in np.linspace(0.0, 0.95, 20):
        selected = [(d, l) for d, l in zip(decisions, te_l) if d.confidence >= threshold]
        coverage = len(selected) / len(te_l)
        if selected:
            exact = sum(d.action == l.preferred_action for d, l in selected) / len(selected)
            acceptable = sum(d.action in l.acceptable_actions for d, l in selected) / len(selected)
            severe_error = sum((d.action not in l.acceptable_actions) * l.severity_of_wrong_action for d, l in selected) / len(selected)
        else:
            exact = acceptable = severe_error = None
        rows.append({
            "threshold": round(float(threshold), 3),
            "coverage": round(float(coverage), 6),
            "exact_accuracy": None if exact is None else round(float(exact), 6),
            "acceptable_rate": None if acceptable is None else round(float(acceptable), 6),
            "severity_weighted_error": None if severe_error is None else round(float(severe_error), 6),
        })

    out = {
        "description": "Selective prediction: only intervene when calibrated top-label confidence exceeds threshold.",
        "temperature": policy.temperature,
        "points": rows,
    }
    (ROOT / "artifacts/selective_eval.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
