from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

from grantshift.serialization import load_policy, read_state

ROOT = Path(__file__).resolve().parents[1]


def test_exported_policy_loads_and_decides():
    path = ROOT / "artifacts/personalized_policy.joblib"
    assert path.exists()
    policy, metadata = load_policy(path)
    state = read_state(ROOT / "examples/state.json")
    probs = policy.predict_proba(state)
    assert abs(sum(probs.values()) - 1.0) < 1e-8
    decision = policy.decide(state)
    assert decision.action in probs
    assert metadata["synthetic_labels"] is True


def test_cli_outputs_machine_readable_json():
    proc = subprocess.run(
        [sys.executable, "-m", "grantshift.cli", "decide", "--state", "examples/state.json", "--model", "artifacts/personalized_policy.joblib"],
        cwd=ROOT, capture_output=True, text=True, check=True,
    )
    payload = json.loads(proc.stdout)
    assert payload["action"]
    assert 0.0 <= payload["confidence"] <= 1.0
    assert abs(sum(payload["probabilities"].values()) - 1.0) < 1e-5


def test_selective_and_diagnostic_artifacts_exist():
    selective = json.loads((ROOT / "artifacts/selective_eval.json").read_text())
    diagnostics = json.loads((ROOT / "artifacts/action_diagnostics.json").read_text())
    assert len(selective["points"]) >= 10
    assert diagnostics["n_test"] == len(__import__("json").loads((ROOT / "grantshiftbench/scenarios/splits.json").read_text())["test"])
    assert "confusion_matrix" in diagnostics


def test_interactive_demo_is_standalone():
    html = (ROOT / "demo/index.html").read_text()
    assert "When should an AI act?" in html
    assert "<script>" in html
    assert "https://" not in html
