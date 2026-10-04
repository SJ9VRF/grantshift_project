from __future__ import annotations
import json
from collections import defaultdict
from pathlib import Path
from agent_eval.suite import build_shift_suite
from agent_eval.agents import AuthorizationFirstAgent, RobustAuthorizationAgent, NoisyAgent
from agent_eval.harness import EvalHarness
from agent_eval.metrics import summarize

ROOT=Path(__file__).resolve().parents[1]

def variant_summary(records):
    out={}
    groups=defaultdict(list)
    for r in records:
        variant=r.outcome.get('env_variant','standard')
        groups[(r.agent_name,variant)].append(r)
    for (agent,variant), rows in groups.items():
        state=[next(g for g in r.graders if g.grader=='state_tracking') for r in rows]
        auth=[next(g for g in r.graders if g.grader=='authorization') for r in rows]
        out.setdefault(agent,{})[variant]={
            'n_trials':len(rows),
            'pass_rate':sum(r.passed for r in rows)/len(rows),
            'state_tracking_rate':sum(g.passed for g in state)/len(state),
            'authorization_pass_rate':sum(g.passed for g in auth)/len(auth),
            'mean_turns':sum(len(r.trajectory) for r in rows)/len(rows),
        }
    return out

def main():
    tasks=build_shift_suite()
    agents=[AuthorizationFirstAgent(), RobustAuthorizationAgent(), NoisyAgent(RobustAuthorizationAgent(),0.08)]
    records=EvalHarness().run_suite(tasks,agents,trials_per_task=5,base_seed=4103)
    result={
        'task_count':len(tasks),
        'trial_count':len(records),
        'overall':summarize(records),
        'by_variant':variant_summary(records),
        'notes':'Controlled sandbox environment-shift evaluation; not frontier-model or human evidence.'
    }
    out=ROOT/'artifacts/cross_environment_eval.json'
    out.write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
