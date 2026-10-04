from agent_eval.suite import build_suite
from agent_eval.agents import PreferenceOnlyAgent, AuthorizationFirstAgent, NoisyAgent
from agent_eval.harness import EvalHarness
from agent_eval.metrics import summarize, pass_at_k, pass_pow_k


def test_trajectory_suite_shape_and_domains():
    tasks=build_suite()
    assert len(tasks)==144
    assert len({t.state.domain for t in tasks})==6
    assert {t.authorization for t in tasks}=={"preauthorized","ask_required","advisory","prohibited"}


def test_authorization_first_solves_deterministic_sandbox():
    rows=EvalHarness().run_suite(build_suite(),[AuthorizationFirstAgent()],trials_per_task=1)
    s=summarize(rows)["authorization_first"]
    assert s["pass_rate"]==1.0
    assert s["authorization_pass_rate"]==1.0
    assert s["recovery_rate"]==1.0


def test_preference_only_exposes_overreach_and_recovery_failure():
    rows=EvalHarness().run_suite(build_suite(),[PreferenceOnlyAgent()],trials_per_task=1)
    s=summarize(rows)["preference_only"]
    assert s["authorization_pass_rate"] < 0.9
    assert s["recovery_rate"] == 0.0


def test_reliability_metrics_diverge_for_imperfect_agent():
    rows=EvalHarness().run_suite(build_suite(),[NoisyAgent(AuthorizationFirstAgent(),0.08)],trials_per_task=5)
    s=summarize(rows)["authorization_first_noisy8"]
    assert s["pass_at_k"]["5"] > s["pass_rate"]
    assert s["pass_pow_k"]["5"] < s["pass_rate"]
    assert pass_at_k(.5,3) == .875
    assert pass_pow_k(.5,3) == .125
