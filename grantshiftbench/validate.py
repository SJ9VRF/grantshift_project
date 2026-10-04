from __future__ import annotations

from collections import Counter
from pathlib import Path
import json

from grantshift.types import Action

REQUIRED_FLOATS = [
    "urgency", "intent_confidence", "execution_confidence", "stakes", "reversibility",
    "expected_benefit", "financial_cost", "social_cost", "privacy_risk", "safety_risk",
    "time_sensitivity",
]


def validate_file(path: str | Path) -> dict:
    path = Path(path)
    errors = []
    ids = []
    domains = Counter()
    actions = Counter()
    with path.open() as f:
        for lineno, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as e:
                errors.append(f"line {lineno}: invalid json: {e}")
                continue
            sid = row.get("scenario_id")
            if not sid:
                errors.append(f"line {lineno}: missing scenario_id")
            ids.append(sid)
            domain = row.get("domain")
            if not domain:
                errors.append(f"line {lineno}: missing domain")
            domains[domain] += 1
            for k in REQUIRED_FLOATS:
                v = row.get(k)
                if not isinstance(v, (int, float)) or not 0 <= float(v) <= 1:
                    errors.append(f"line {lineno}: {k} must be numeric in [0,1]")
            label = row.get("label", {})
            preferred = label.get("preferred_action")
            if preferred not in {a.value for a in Action}:
                errors.append(f"line {lineno}: invalid preferred_action={preferred}")
            actions[preferred] += 1
            acceptable = set(label.get("acceptable_actions", []))
            bad = set(label.get("bad_actions", []))
            if preferred and preferred not in acceptable:
                errors.append(f"line {lineno}: preferred action is not acceptable")
            if acceptable & bad:
                errors.append(f"line {lineno}: action cannot be both acceptable and bad")
            sev = label.get("severity_of_wrong_action")
            if not isinstance(sev, (int, float)) or not 0 <= float(sev) <= 1:
                errors.append(f"line {lineno}: severity_of_wrong_action must be in [0,1]")
    duplicate_ids = [k for k, v in Counter(ids).items() if k is not None and v > 1]
    if duplicate_ids:
        errors.append(f"duplicate scenario ids: {duplicate_ids[:10]}")
    return {
        "path": str(path),
        "valid": not errors,
        "n": len(ids),
        "domains": dict(domains),
        "preferred_actions": dict(actions),
        "errors": errors,
    }


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("path")
    args = p.parse_args()
    result = validate_file(args.path)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["valid"] else 1)
