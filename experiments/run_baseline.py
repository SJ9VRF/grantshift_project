import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from evaluation.metrics import evaluate
from grantshift.policy.heuristic import decide
from grantshiftbench.loaders.jsonl import load_jsonl


if __name__ == "__main__":
    states, labels = load_jsonl(ROOT / "grantshiftbench/scenarios/v0.jsonl")
    decisions = [decide(s) for s in states]
    result = evaluate([d.action for d in decisions], labels)

    for s, d, label in zip(states, decisions, labels):
        print(f"{s.scenario_id:>12} | pred={d.action.value:<10} | gold={label.preferred_action.value:<10} | risk={d.risk:.2f} | {'; '.join(d.reasons)}")

    print("\nAggregate metrics")
    for k, v in result.__dict__.items():
        print(f"{k}: {v:.3f}")
