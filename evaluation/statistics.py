from __future__ import annotations

from collections import defaultdict
import random
import numpy as np

from grantshift.types import Action, ScenarioLabel, AgentState
from evaluation.metrics import evaluate
from evaluation.advanced_metrics import expected_calibration_error, mean_wrong_action_severity


def bootstrap_metric(preds, labels, metric_fn, n_boot=1000, seed=2026, alpha=0.05):
    """Deterministic non-parametric bootstrap confidence interval."""
    preds, labels = list(preds), list(labels)
    if len(preds) != len(labels) or not preds:
        raise ValueError("non-empty predictions and labels of equal size required")
    rng = random.Random(seed)
    vals = []
    n = len(preds)
    for _ in range(n_boot):
        idx = [rng.randrange(n) for _ in range(n)]
        vals.append(float(metric_fn([preds[i] for i in idx], [labels[i] for i in idx])))
    lo, hi = np.quantile(vals, [alpha / 2, 1 - alpha / 2])
    return {"low": float(lo), "high": float(hi), "n_boot": n_boot}


def accuracy_ci(preds, labels, **kwargs):
    return bootstrap_metric(preds, labels, lambda p, l: evaluate(p, l).accuracy, **kwargs)


def acceptable_ci(preds, labels, **kwargs):
    return bootstrap_metric(preds, labels, lambda p, l: evaluate(p, l).acceptable_action_rate, **kwargs)


def grouped_metrics(states: list[AgentState], preds: list[Action], labels: list[ScenarioLabel]):
    groups = defaultdict(list)
    for i, s in enumerate(states):
        groups[s.domain].append(i)
    out = {}
    for name, idx in sorted(groups.items()):
        p = [preds[i] for i in idx]
        l = [labels[i] for i in idx]
        r = evaluate(p, l)
        out[name] = {
            **r.__dict__,
            "n": len(idx),
            "mean_wrong_action_severity": mean_wrong_action_severity(p, l),
        }
    return out


def calibration_report(confidences, preds, labels, bins=10):
    correctness = [p == l.preferred_action for p, l in zip(preds, labels)]
    return {
        "ece": expected_calibration_error(confidences, correctness, bins=bins),
        "mean_confidence": float(np.mean(confidences)),
        "empirical_accuracy": float(np.mean(correctness)),
        "brier_toplabel": float(np.mean((np.asarray(confidences) - np.asarray(correctness, dtype=float)) ** 2)),
    }
