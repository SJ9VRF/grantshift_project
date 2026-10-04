from __future__ import annotations
import json
from pathlib import Path
from agent_eval.suite import build_suite
from agent_eval.agents import PreferenceOnlyAgent, AuthorizationFirstAgent, AlwaysAskAgent, NoisyAgent
from agent_eval.harness import EvalHarness
from agent_eval.metrics import summarize
from posttraining.failure_mining import mine
from posttraining.build_training_data import build
from posttraining.prioritize_incidents import prioritize
from posttraining.reward import trajectory_reward

out=Path("artifacts"); out.mkdir(exist_ok=True)
tasks=build_suite()
agents=[PreferenceOnlyAgent(),AuthorizationFirstAgent(),AlwaysAskAgent(),NoisyAgent(AuthorizationFirstAgent(),0.08)]
records=EvalHarness().run_suite(tasks,agents,trials_per_task=5)
trial_dicts=[r.to_dict() for r in records]
for r in trial_dicts: r["trajectory_reward"]=trajectory_reward(r)
(out/"trajectory_trials.json").write_text(json.dumps(trial_dicts,indent=2))
summary=summarize(records)
(out/"trajectory_eval.json").write_text(json.dumps({"n_tasks":len(tasks),"trials_per_task":5,"summary":summary},indent=2))
inc=mine(out/"trajectory_trials.json",out/"incident_bank.json")
ranking=prioritize(out/"incident_bank.json",out/"incident_priorities.json")
pairs=build(out/"incident_bank.json",out/"failure_training_pairs.jsonl")
print(json.dumps({"n_tasks":len(tasks),"n_trials":len(records),"n_incidents":len(inc),"n_training_pairs":len(pairs),"incident_priorities":ranking,"summary":summary},indent=2))
