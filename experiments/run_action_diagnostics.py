from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

from grantshift.policy.learned import LearnedPolicy
from grantshift.types import Action
from grantshiftbench.loaders.jsonl import load_scenarios, select_split

ROOT = Path(__file__).resolve().parents[1]
ACTIONS = list(Action)


def main():
    states, labels = load_scenarios(ROOT / "grantshiftbench/scenarios/v1.jsonl")
    tr_s, tr_l = select_split(states, labels, ROOT / "grantshiftbench/scenarios/splits.json", "train")
    te_s, te_l = select_split(states, labels, ROOT / "grantshiftbench/scenarios/splits.json", "test")
    policy = LearnedPolicy(include_personalization=True).fit(tr_s, [l.preferred_action for l in tr_l])
    preds = [policy.decide(s).action for s in te_s]

    matrix = {a.value: {b.value: 0 for b in ACTIONS} for a in ACTIONS}
    for gold, pred in zip([l.preferred_action for l in te_l], preds):
        matrix[gold.value][pred.value] += 1

    per_action = {}
    for a in ACTIONS:
        tp = sum(1 for p, l in zip(preds, te_l) if p == a and l.preferred_action == a)
        fp = sum(1 for p, l in zip(preds, te_l) if p == a and l.preferred_action != a)
        fn = sum(1 for p, l in zip(preds, te_l) if p != a and l.preferred_action == a)
        precision = tp / (tp + fp) if tp + fp else None
        recall = tp / (tp + fn) if tp + fn else None
        f1 = None if precision is None or recall is None or precision + recall == 0 else 2 * precision * recall / (precision + recall)
        per_action[a.value] = {
            "support": sum(1 for l in te_l if l.preferred_action == a),
            "predicted": sum(1 for p in preds if p == a),
            "precision": precision,
            "recall": recall,
            "f1": f1,
        }

    errors = []
    for s, l, p in zip(te_s, te_l, preds):
        if p != l.preferred_action:
            errors.append({
                "scenario_id": s.scenario_id,
                "domain": s.domain,
                "gold": l.preferred_action.value,
                "pred": p.value,
                "acceptable": [a.value for a in l.acceptable_actions],
                "severity": l.severity_of_wrong_action,
                "goal": s.goal,
            })
    errors.sort(key=lambda x: (-x["severity"], x["domain"], x["scenario_id"]))

    out = {
        "n_test": len(te_s),
        "gold_distribution": dict(Counter(l.preferred_action.value for l in te_l)),
        "prediction_distribution": dict(Counter(p.value for p in preds)),
        "confusion_matrix": matrix,
        "per_action": per_action,
        "errors": errors,
    }
    path = ROOT / "artifacts/action_diagnostics.json"
    path.write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
