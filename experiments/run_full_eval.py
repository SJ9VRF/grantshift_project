from pathlib import Path
import json, sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from grantshiftbench.loaders.jsonl import load_scenarios, select_split
from grantshift.policy.heuristic import decide as heuristic_decide
from grantshift.policy.learned import LearnedPolicy
from evaluation.metrics import evaluate
from evaluation.advanced_metrics import intervention_precision_recall, mean_wrong_action_severity
from evaluation.statistics import accuracy_ci, acceptable_ci, grouped_metrics, calibration_report
from evaluation.frontier_metrics import intervention_frontier_metrics


def pack(name, states, preds, labels, conf=None, extra=None):
    b = evaluate(preds, labels).__dict__
    b.update(intervention_precision_recall(preds, labels))
    b["mean_wrong_action_severity"] = mean_wrong_action_severity(preds, labels)
    b["accuracy_ci95"] = accuracy_ci(preds, labels, n_boot=1000)
    b["acceptable_ci95"] = acceptable_ci(preds, labels, n_boot=1000)
    b["by_domain"] = grouped_metrics(states, preds, labels)
    b.update(intervention_frontier_metrics(states, preds, labels))
    if conf is not None:
        b["calibration"] = calibration_report(conf, preds, labels)
    if extra:
        b.update(extra)
    return name, b


def main():
    data = ROOT / "grantshiftbench/scenarios/v1.jsonl"
    splits = ROOT / "grantshiftbench/scenarios/splits.json"
    states, labels = load_scenarios(data)
    tr_s, tr_l = select_split(states, labels, splits, "train")
    dv_s, dv_l = select_split(states, labels, splits, "dev")
    te_s, te_l = select_split(states, labels, splits, "test")

    results = {
        "metadata": {
            "benchmark": "GrantShiftBench v1",
            "train_n": len(tr_s),
            "dev_n": len(dv_s),
            "test_n": len(te_s),
            "bootstrap_samples": 1000,
            "calibration_protocol": "held-out dev-set scalar temperature scaling",
            "synthetic_labels": True,
        }
    }

    hp = [heuristic_decide(s) for s in te_s]
    n, b = pack("heuristic", te_s, [d.action for d in hp], te_l, [d.confidence for d in hp])
    results[n] = b

    generic = LearnedPolicy(include_personalization=False).fit(tr_s, [l.preferred_action for l in tr_l])
    gd = [generic.decide(s) for s in te_s]
    n, b = pack("generic_learned", te_s, [d.action for d in gd], te_l, [d.confidence for d in gd])
    results[n] = b

    personalized = LearnedPolicy(include_personalization=True).fit(tr_s, [l.preferred_action for l in tr_l])
    pd = [personalized.decide(s) for s in te_s]
    n, b = pack("personalized_learned", te_s, [d.action for d in pd], te_l, [d.confidence for d in pd])
    results[n] = b

    calibrated = LearnedPolicy(include_personalization=True).fit(tr_s, [l.preferred_action for l in tr_l])
    calibrated.calibrate(dv_s, [l.preferred_action for l in dv_l])
    cd = [calibrated.decide(s) for s in te_s]
    n, b = pack(
        "personalized_calibrated",
        te_s,
        [d.action for d in cd],
        te_l,
        [d.confidence for d in cd],
        {"temperature": calibrated.temperature},
    )
    results[n] = b

    out = ROOT / "artifacts/eval_results.json"
    out.write_text(json.dumps(results, indent=2))
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
