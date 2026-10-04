# Trajectory-level agent evaluation

GrantShift the v1.3 milestone added a small but complete agent-evaluation harness around the preference-permission problem. The goal is not to pretend that a symbolic sandbox is a production browser or computer-use environment. The goal is to make the evaluation object match an agent system rather than a single classifier decision.

Each **task** defines an initial user state, authorization boundary, reversibility, and end-state requirement. Each **trial** records a full **trajectory** of actions and observations. Grading operates on both the trajectory and the final **outcome**. The harness supports repeated trials and reports first-try success as well as pass@k and pass^k-style reliability summaries.

The grader stack intentionally mixes concerns rather than collapsing them into one score:

- `authorization`: whether the agent attempted an action outside the active permission envelope;
- `outcome`: whether the final environment state satisfies the task without forbidden mutation;
- `interaction_efficiency`: redundant asks/interventions;
- `recovery`: whether ask-required tasks correctly transition from clarification to action, or to deferral when the action is irreversible.

The deterministic sandbox contains 144 tasks across email, calendar, travel, shopping, files, and communication. Every task is run five times for every policy adapter. A seeded noisy wrapper exists specifically to make reliability metrics meaningful.

This suite is a **mechanism and infrastructure test**. It does not substitute for real browser/computer-use environments, human users, or frontier-model trajectories.

## Why outcome verification matters

A transcript saying "done" is not success. The harness grades `external_change_committed` in environment state. This mirrors the broader principle that agent evaluation should distinguish claimed completion from verified world state.

## Capability and regression use

The same task bank can be used in two modes:

- **capability evals**: difficult subsets where pass rate is intentionally below saturation;
- **regression evals**: stable authorization and recovery cases expected to remain near 100% after a behavior change.

The release keeps both detailed trial records and aggregate metrics so failures can be converted into targeted regression cases.
