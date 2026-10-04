from __future__ import annotations

from collections import Counter
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "grantshiftbench/scenarios/v1.jsonl"
SPLITS = ROOT / "grantshiftbench/scenarios/splits.json"
OUT = ROOT / "artifacts/leakage_audit.json"


def canonical_input(row):
    # Only model-visible information; explicitly excludes labels and scenario_id.
    keep = {
        k: row[k]
        for k in [
            "domain", "goal", "urgency", "intent_confidence", "execution_confidence",
            "stakes", "reversibility", "expected_benefit", "financial_cost", "social_cost",
            "privacy_risk", "safety_risk", "time_sensitivity", "user_profile", "metadata"
        ]
    }
    return json.dumps(keep, sort_keys=True, separators=(",", ":"))


def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()


def main():
    rows = [json.loads(x) for x in DATA.read_text().splitlines() if x.strip()]
    by_id = {r["scenario_id"]: r for r in rows}
    splits = json.loads(SPLITS.read_text())
    iid = {k: set(splits[k]) for k in ("train", "dev", "test")}

    overlap = {
        "train_dev": sorted(iid["train"] & iid["dev"]),
        "train_test": sorted(iid["train"] & iid["test"]),
        "dev_test": sorted(iid["dev"] & iid["test"]),
    }
    fp = {}
    for name, ids in iid.items():
        fp[name] = Counter(digest(canonical_input(by_id[i])) for i in ids)
    exact_dup = {
        "train_dev": sorted(set(fp["train"]) & set(fp["dev"])),
        "train_test": sorted(set(fp["train"]) & set(fp["test"])),
        "dev_test": sorted(set(fp["dev"]) & set(fp["test"])),
    }

    # Check that label-only fields are never part of the vectorizer source.
    vectorizer = (ROOT / "grantshift/features/vectorize.py").read_text()
    suspicious_tokens = [t for t in ["preferred_action", "acceptable_actions", "bad_actions", "severity_of_wrong_action"] if t in vectorizer]

    report = {
        "split_version": splits.get("version"),
        "split_seed": splits.get("seed"),
        "n_rows": len(rows),
        "iid_sizes": {k: len(v) for k, v in iid.items()},
        "id_overlap_counts": {k: len(v) for k, v in overlap.items()},
        "exact_input_duplicate_counts": {k: len(v) for k, v in exact_dup.items()},
        "label_tokens_in_vectorizer": suspicious_tokens,
        "passes": all(len(v) == 0 for v in overlap.values()) and all(len(v) == 0 for v in exact_dup.values()) and not suspicious_tokens,
        "limitations": [
            "Synthetic scenarios share a common generator and oracle by design; zero exact duplication does not imply independence of generative mechanism.",
            "OOD evaluations are reported separately to probe generalization beyond IID splitting."
        ],
    }
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    if not report["passes"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
