from __future__ import annotations
import json
from pathlib import Path
from grantshift.types import Action, AgentState, AutonomyProfile
from agent_eval.schema import AgentTask, TrajectoryStep
from agent_eval.environment import PersonalActionEnvironment
from agent_eval.graders import grade_trial
ROOT=Path(__file__).resolve().parents[1]

def run_case(c):
    state=AgentState(
        scenario_id=c['name'], domain='email', goal='rubric regression', urgency=.5,
        intent_confidence=.9, execution_confidence=.9, stakes=.5,
        reversibility=1.0 if c['recoverable'] else 0.0, expected_benefit=.5,
        user_profile=AutonomyProfile({'email':Action.ACT},.5,Action.ACT),
        metadata={'authorization':c['initial_auth'],'recoverable':c['recoverable'],'env_variant':c['variant']})
    task=AgentTask(c['name'],state,c['initial_auth'],c['recoverable'],True,6,['rubric'])
    env=PersonalActionEnvironment(task); traj=[]; obs='Task initialized.'
    for i,a in enumerate(c['actions']):
        before=env.snapshot(); obs=env.step(Action(a)); after=env.snapshot()
        traj.append(TrajectoryStep(i,Action(a),obs,before,after,0.0))
        if after['done']: break
    grades=grade_trial(task,traj,env.snapshot())
    got={g.grader:g.passed for g in grades}
    ok=all(got[k] == v for k,v in c['expect'].items())
    return {'name':c['name'],'expected':c['expect'],'got':got,'passed':ok}

def main():
    cases=json.loads((ROOT/'evaluation/grader_rubric_cases.json').read_text())
    rows=[run_case(c) for c in cases]
    report={'n_cases':len(rows),'passed_cases':sum(r['passed'] for r in rows),'agreement':sum(r['passed'] for r in rows)/len(rows),'cases':rows}
    (ROOT/'artifacts/grader_rubric_regression.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))
    raise SystemExit(0 if report['agreement']==1.0 else 1)
if __name__=='__main__': main()
