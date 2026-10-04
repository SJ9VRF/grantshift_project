from __future__ import annotations

import json
from pathlib import Path

from grantshift.policy.learned import LearnedPolicy
from grantshift.serialization import save_policy
from grantshiftbench.loaders.jsonl import load_scenarios, select_split

ROOT = Path(__file__).resolve().parents[1]


def main():
    states, labels = load_scenarios(ROOT / "grantshiftbench/scenarios/v1.jsonl")
    tr_s, tr_l = select_split(states, labels, ROOT / "grantshiftbench/scenarios/splits.json", "train")
    dv_s, dv_l = select_split(states, labels, ROOT / "grantshiftbench/scenarios/splits.json", "dev")
    policy = LearnedPolicy(include_personalization=True).fit(tr_s, [l.preferred_action for l in tr_l])
    policy.calibrate(dv_s, [l.preferred_action for l in dv_l])
    metadata = {
        "name": "personalized_calibrated",
        "benchmark": "GrantShiftBench v1",
        "train_examples": len(tr_s),
        "calibration_examples": len(dv_s),
        "synthetic_labels": True,
        "research_only": True,
    }
    path = save_policy(policy, ROOT / "artifacts/personalized_policy.joblib", metadata)
    (ROOT / "artifacts/personalized_policy.metadata.json").write_text(json.dumps(metadata | {"temperature": policy.temperature}, indent=2))
    print(path)


if __name__ == "__main__":
    main()
