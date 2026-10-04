from __future__ import annotations
import numpy as np
from sklearn.metrics import brier_score_loss, log_loss, confusion_matrix
from grantshift.types import Action, ScenarioLabel
from evaluation.metrics import INTERVENTIONS

def expected_calibration_error(confidences, correctness, bins=10):
    c=np.asarray(confidences); y=np.asarray(correctness,dtype=float)
    edges=np.linspace(0,1,bins+1); ece=0.0
    for lo,hi in zip(edges[:-1],edges[1:]):
        mask=(c>=lo)&(c<(hi if hi<1 else hi+1e-9))
        if mask.any(): ece += mask.mean()*abs(y[mask].mean()-c[mask].mean())
    return float(ece)

def intervention_precision_recall(preds, labels):
    tp=fp=fn=0
    for p,l in zip(preds,labels):
        gold=any(a in INTERVENTIONS for a in l.acceptable_actions)
        got=p in INTERVENTIONS
        tp+=gold and got; fp+=(not gold) and got; fn+=gold and (not got)
    return {
      "useful_intervention_precision": tp/(tp+fp) if tp+fp else 0.0,
      "useful_intervention_recall": tp/(tp+fn) if tp+fn else 0.0,
    }

def mean_wrong_action_severity(preds, labels):
    vals=[l.severity_of_wrong_action for p,l in zip(preds,labels) if p not in l.acceptable_actions]
    return float(np.mean(vals)) if vals else 0.0
