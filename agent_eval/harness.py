from __future__ import annotations
import time
from .environment import PersonalActionEnvironment
from .graders import grade_trial
from .schema import TrialRecord, TrajectoryStep

class EvalHarness:
    def run_trial(self, task, agent, trial_id: int, seed: int) -> TrialRecord:
        env = PersonalActionEnvironment(task)
        agent.reset(task, seed)
        observation = "Task initialized."
        trajectory = []
        for turn in range(task.max_turns):
            before = env.snapshot()
            t0 = time.perf_counter()
            action = agent.act(observation, before)
            latency_ms = (time.perf_counter() - t0) * 1000
            observation = env.step(action)
            after = env.snapshot()
            trajectory.append(TrajectoryStep(turn, action, observation, before, after, latency_ms))
            if after["done"]: break
        outcome = env.snapshot()
        graders = grade_trial(task, trajectory, outcome)
        # Safety and outcome are hard requirements; efficiency is diagnostic.
        passed = all(next(g.passed for g in graders if g.grader == name) for name in ["authorization", "outcome", "recovery", "state_tracking"])
        return TrialRecord(task.task_id, trial_id, agent.name, seed, trajectory, outcome, graders, passed)

    def run_suite(self, tasks, agents, trials_per_task=5, base_seed=1729):
        records = []
        for ai, agent in enumerate(agents):
            for ti, task in enumerate(tasks):
                for trial in range(trials_per_task):
                    seed = base_seed + ai * 100000 + ti * 100 + trial
                    records.append(self.run_trial(task, agent, trial, seed))
        return records
