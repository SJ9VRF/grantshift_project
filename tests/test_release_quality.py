from pathlib import Path

from grantshiftbench.validate import validate_file
from grantshiftbench.loaders.jsonl import load_scenarios, select_split
from grantshift.policy.learned import LearnedPolicy
from evaluation.statistics import grouped_metrics, accuracy_ci

ROOT = Path(__file__).resolve().parents[1]


def test_benchmark_schema_is_valid():
    r = validate_file(ROOT / "grantshiftbench/scenarios/v1.jsonl")
    assert r["valid"], r["errors"]
    assert r["n"] == 600
    assert len(r["domains"]) == 12


def test_contrast_schema_is_valid():
    r = validate_file(ROOT / "grantshiftbench/scenarios/contrast_v1.jsonl")
    assert r["valid"], r["errors"]
    assert r["n"] >= 100


def test_temperature_calibration_uses_dev_and_is_finite():
    s, l = load_scenarios(ROOT / "grantshiftbench/scenarios/v1.jsonl")
    sp = ROOT / "grantshiftbench/scenarios/splits.json"
    tr, tl = select_split(s, l, sp, "train")
    dv, dl = select_split(s, l, sp, "dev")
    p = LearnedPolicy(include_personalization=True).fit(tr, [x.preferred_action for x in tl])
    p.calibrate(dv, [x.preferred_action for x in dl])
    assert 0.1 <= p.temperature <= 10.0
    probs = p.predict_proba(dv[0])
    assert abs(sum(probs.values()) - 1.0) < 1e-9


def test_domain_metrics_cover_all_test_domains():
    s, l = load_scenarios(ROOT / "grantshiftbench/scenarios/v1.jsonl")
    sp = ROOT / "grantshiftbench/scenarios/splits.json"
    tr, tl = select_split(s, l, sp, "train")
    te, el = select_split(s, l, sp, "test")
    p = LearnedPolicy(include_personalization=True).fit(tr, [x.preferred_action for x in tl])
    preds = [p.decide(x).action for x in te]
    gm = grouped_metrics(te, preds, el)
    assert set(gm) == {x.domain for x in te}
    assert all(v["n"] > 0 for v in gm.values())


def test_bootstrap_ci_contains_point_accuracy():
    s, l = load_scenarios(ROOT / "grantshiftbench/scenarios/v1.jsonl")
    sp = ROOT / "grantshiftbench/scenarios/splits.json"
    tr, tl = select_split(s, l, sp, "train")
    te, el = select_split(s, l, sp, "test")
    p = LearnedPolicy(include_personalization=True).fit(tr, [x.preferred_action for x in tl])
    preds = [p.decide(x).action for x in te]
    acc = sum(a == b.preferred_action for a, b in zip(preds, el)) / len(el)
    ci = accuracy_ci(preds, el, n_boot=250)
    assert ci["low"] <= acc <= ci["high"]


def test_split_protocol_has_no_overlap_and_ood_specs():
    import json
    sp = json.loads((ROOT / "grantshiftbench/scenarios/splits.json").read_text())
    assert sp["version"] == "2.0"
    tr, dv, te = map(set, (sp["train"], sp["dev"], sp["test"]))
    assert not (tr & dv or tr & te or dv & te)
    assert len(tr | dv | te) == 600
    assert set(sp["ood_domain"]["heldout_domains"]) == {"privacy", "financial", "high_stakes"}
    assert set(sp["ood_trigger"]["heldout_triggers"]) == {"privacy_change", "new_information"}


def test_leakage_audit_passes():
    import json
    p = ROOT / "artifacts/leakage_audit.json"
    if not p.exists():
        import subprocess, sys
        subprocess.run([sys.executable, "scripts/leakage_audit.py"], cwd=ROOT, check=True)
    r = json.loads(p.read_text())
    assert r["passes"] is True
    assert all(v == 0 for v in r["id_overlap_counts"].values())
    assert all(v == 0 for v in r["exact_input_duplicate_counts"].values())
