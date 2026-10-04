from agent_eval.suite import build_shift_suite
from agent_eval.agents import AuthorizationFirstAgent, RobustAuthorizationAgent
from agent_eval.harness import EvalHarness

def test_shift_suite_has_all_variants():
    tasks=build_shift_suite()
    variants={t.state.metadata['env_variant'] for t in tasks}
    assert variants == {'standard','delayed_confirmation','transient_tool_failure','revoked_after_confirmation'}
    assert len(tasks) == 90

def test_robust_policy_handles_shift_suite_better():
    tasks=build_shift_suite()
    recs=EvalHarness().run_suite(tasks,[AuthorizationFirstAgent(),RobustAuthorizationAgent()],trials_per_task=1)
    by={}
    for r in recs: by.setdefault(r.agent_name,[]).append(r)
    simple=sum(r.passed for r in by['authorization_first'])/len(by['authorization_first'])
    robust=sum(r.passed for r in by['robust_authorization_first'])/len(by['robust_authorization_first'])
    assert robust > simple
    assert robust >= 0.95
