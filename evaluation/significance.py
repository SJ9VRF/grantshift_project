from __future__ import annotations
import math
import random
from typing import Sequence
from grantshift.types import Action, ScenarioLabel


def _correct(pred: Action, label: ScenarioLabel) -> int:
    return int(pred == label.preferred_action)


def paired_accuracy_difference(pred_a: Sequence[Action], pred_b: Sequence[Action], labels: Sequence[ScenarioLabel], n_boot: int = 10000, seed: int = 7) -> dict:
    if not (len(pred_a) == len(pred_b) == len(labels)):
        raise ValueError("length mismatch")
    n = len(labels)
    a = [_correct(p, l) for p, l in zip(pred_a, labels)]
    b = [_correct(p, l) for p, l in zip(pred_b, labels)]
    delta = sum(b)/n - sum(a)/n
    rng = random.Random(seed)
    boots = []
    for _ in range(n_boot):
        idx = [rng.randrange(n) for _ in range(n)]
        da = sum(a[i] for i in idx)/n
        db = sum(b[i] for i in idx)/n
        boots.append(db-da)
    boots.sort()
    lo = boots[int(0.025*(n_boot-1))]
    hi = boots[int(0.975*(n_boot-1))]
    return {"delta_accuracy": delta, "ci95": [lo, hi], "bootstrap_samples": n_boot}


def mcnemar_exact(pred_a: Sequence[Action], pred_b: Sequence[Action], labels: Sequence[ScenarioLabel]) -> dict:
    """Two-sided exact McNemar test using a Binomial(n, 0.5) null."""
    b = 0  # A correct, B wrong
    c = 0  # A wrong, B correct
    for pa, pb, l in zip(pred_a, pred_b, labels):
        ca = pa == l.preferred_action
        cb = pb == l.preferred_action
        if ca and not cb:
            b += 1
        elif cb and not ca:
            c += 1
    n = b + c
    if n == 0:
        return {"a_correct_b_wrong": b, "a_wrong_b_correct": c, "discordant": 0, "p_value_two_sided": 1.0}
    k = min(b, c)
    tail = sum(math.comb(n, i) for i in range(0, k+1)) / (2 ** n)
    p = min(1.0, 2.0 * tail)
    return {"a_correct_b_wrong": b, "a_wrong_b_correct": c, "discordant": n, "p_value_two_sided": p}
