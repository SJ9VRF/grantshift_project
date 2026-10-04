from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import json
import random

ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = ROOT / "grantshiftbench/scenarios/v1.jsonl"
OUT = ROOT / "grantshiftbench/scenarios/splits.json"


def load_rows():
    return [json.loads(x) for x in SCENARIOS.read_text().splitlines() if x.strip()]


def stratified_iid(rows, seed: int = 20260923):
    """Deterministic stratified 70/15/15 split over domain x preferred action.

    We shuffle within strata so generator ordering cannot determine split membership.
    """
    rng = random.Random(seed)
    buckets = defaultdict(list)
    for r in rows:
        key = (r["domain"], r["label"]["preferred_action"])
        buckets[key].append(r["scenario_id"])
    train, dev, test = [], [], []
    for ids in buckets.values():
        rng.shuffle(ids)
        n = len(ids)
        n_train = int(round(n * 0.70))
        n_dev = int(round(n * 0.15))
        # Guarantee all non-trivial strata are represented where possible.
        if n >= 3:
            n_train = min(max(1, n_train), n - 2)
            n_dev = min(max(1, n_dev), n - n_train - 1)
        train.extend(ids[:n_train])
        dev.extend(ids[n_train:n_train+n_dev])
        test.extend(ids[n_train+n_dev:])
    rng.shuffle(train); rng.shuffle(dev); rng.shuffle(test)
    return {"train": train, "dev": dev, "test": test}


def ood_domain(rows):
    heldout = {"privacy", "financial", "high_stakes"}
    train = [r["scenario_id"] for r in rows if r["domain"] not in heldout]
    test = [r["scenario_id"] for r in rows if r["domain"] in heldout]
    return {"train": train, "test": test, "heldout_domains": sorted(heldout)}


def ood_trigger(rows):
    heldout = {"privacy_change", "new_information"}
    train = [r["scenario_id"] for r in rows if r["metadata"].get("trigger") not in heldout]
    test = [r["scenario_id"] for r in rows if r["metadata"].get("trigger") in heldout]
    return {"train": train, "test": test, "heldout_triggers": sorted(heldout)}


def main():
    rows = load_rows()
    payload = {
        "version": "2.0",
        "seed": 20260923,
        "iid": stratified_iid(rows),
        "ood_domain": ood_domain(rows),
        "ood_trigger": ood_trigger(rows),
    }
    # Backwards-compatible aliases used by existing scripts.
    payload.update(payload["iid"])
    OUT.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"wrote split protocol to {OUT}")
    for name, split in payload.items():
        if isinstance(split, dict) and "train" in split:
            print(name, {k: len(v) if isinstance(v, list) and k in {"train","dev","test"} else v for k,v in split.items()})


if __name__ == "__main__":
    main()
