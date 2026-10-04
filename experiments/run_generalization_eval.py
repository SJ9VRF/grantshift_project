from __future__ import annotations

from pathlib import Path
import json
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from grantshiftbench.loaders.jsonl import load_scenarios
from grantshift.policy.learned import LearnedPolicy
from evaluation.metrics import evaluate
from evaluation.advanced_metrics import intervention_precision_recall, mean_wrong_action_severity
from evaluation.statistics import calibration_report


def select(states, labels, ids):
    ids = set(ids)
    pairs = [(s,l) for s,l in zip(states,labels) if s.scenario_id in ids]
    return [s for s,_ in pairs], [l for _,l in pairs]


def split_calibration(states, labels, seed=903):
    idx = list(range(len(states)))
    random.Random(seed).shuffle(idx)
    n_cal = max(20, int(0.15 * len(idx)))
    cal_idx, train_idx = set(idx[:n_cal]), idx[n_cal:]
    tr_s=[states[i] for i in train_idx]; tr_l=[labels[i] for i in train_idx]
    ca_s=[states[i] for i in cal_idx]; ca_l=[labels[i] for i in cal_idx]
    return tr_s,tr_l,ca_s,ca_l


def score(model, states, labels):
    decisions=[model.decide(s) for s in states]
    preds=[d.action for d in decisions]
    b=evaluate(preds,labels).__dict__
    b.update(intervention_precision_recall(preds,labels))
    b["mean_wrong_action_severity"]=mean_wrong_action_severity(preds,labels)
    b["calibration"]=calibration_report([d.confidence for d in decisions],preds,labels)
    return b


def run_protocol(name, spec, states, labels):
    base_s, base_l = select(states, labels, spec["train"])
    test_s, test_l = select(states, labels, spec["test"])
    tr_s,tr_l,ca_s,ca_l=split_calibration(base_s,base_l)
    out={"train_n":len(tr_s),"calibration_n":len(ca_s),"test_n":len(test_s)}
    for personalized in (False,True):
        model=LearnedPolicy(include_personalization=personalized).fit(tr_s,[l.preferred_action for l in tr_l])
        model.calibrate(ca_s,[l.preferred_action for l in ca_l])
        out["personalized" if personalized else "generic"]=score(model,test_s,test_l)
    for k,v in spec.items():
        if k.startswith("heldout_"): out[k]=v
    return name,out


def main():
    states,labels=load_scenarios(ROOT/"grantshiftbench/scenarios/v1.jsonl")
    splits=json.loads((ROOT/"grantshiftbench/scenarios/splits.json").read_text())
    results={"metadata":{"synthetic_labels":True,"purpose":"stress-test generalization; not evidence of real-user validity"}}
    for name in ("ood_domain","ood_trigger"):
        k,v=run_protocol(name,splits[name],states,labels); results[k]=v
    out=ROOT/"artifacts/generalization_results.json"
    out.write_text(json.dumps(results,indent=2)+"\n")
    print(json.dumps(results,indent=2))

if __name__=="__main__": main()
