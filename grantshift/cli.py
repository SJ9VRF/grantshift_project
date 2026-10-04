from __future__ import annotations

import argparse
import json
from pathlib import Path

from grantshift.policy.heuristic import decide as heuristic_decide
from grantshift.serialization import load_policy, read_state


def _decision_payload(decision, probs=None, metadata=None):
    out = {
        "action": decision.action.value,
        "confidence": round(float(decision.confidence), 6),
        "risk": round(float(decision.risk), 6),
        "utility": round(float(decision.utility), 6),
        "reasons": list(decision.reasons),
    }
    if probs is not None:
        out["probabilities"] = {
            a.value: round(float(p), 6)
            for a, p in sorted(probs.items(), key=lambda kv: kv[1], reverse=True)
        }
    if metadata:
        out["model_metadata"] = metadata
    return out


def cmd_decide(args):
    state = read_state(args.state)
    if args.policy == "heuristic":
        d = heuristic_decide(state)
        payload = _decision_payload(d)
    else:
        policy, metadata = load_policy(args.model)
        probs = policy.predict_proba(state)
        d = policy.decide(state)
        payload = _decision_payload(d, probs=probs, metadata=metadata)
    print(json.dumps(payload, indent=2))


def cmd_model_info(args):
    policy, metadata = load_policy(args.model)
    payload = {
        "include_personalization": policy.include_personalization,
        "calibrated": policy.calibrated,
        "temperature": policy.temperature,
        "feature_groups": sorted(policy.feature_groups) if policy.feature_groups else None,
        "metadata": metadata,
    }
    print(json.dumps(payload, indent=2))


def build_parser():
    parser = argparse.ArgumentParser(prog="grantshift-agent", description="GrantShift dynamic-authorization research CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    decide = sub.add_parser("decide", help="make a proactive intervention decision from a JSON state")
    decide.add_argument("--state", required=True, help="path to a JSON AgentState")
    decide.add_argument("--policy", choices=["learned", "heuristic"], default="learned")
    decide.add_argument("--model", default="artifacts/personalized_policy.joblib", help="learned policy bundle")
    decide.set_defaults(func=cmd_decide)

    info = sub.add_parser("model-info", help="inspect a saved learned policy bundle")
    info.add_argument("--model", default="artifacts/personalized_policy.joblib")
    info.set_defaults(func=cmd_model_info)
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
