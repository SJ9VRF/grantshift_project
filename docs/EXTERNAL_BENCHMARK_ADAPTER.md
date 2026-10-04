# External-environment adapter plan

GrantShift is not a replacement for realistic mobile, coding, or long-horizon agent benchmarks. The next empirical step is to inject authorization transitions into an existing environment without changing its underlying task objective.

## Required adapter interface

An adapter must expose:

1. `reset(base_task)` -> deterministic initial environment snapshot;
2. `apply_authorization_event(event)` -> grant/revoke/expire/supersede/confirm a **specific action scope/version**;
3. `agent_observation()` -> only information naturally available to the evaluated agent;
4. `step(agent_action)` -> tool/environment transition;
5. `snapshot()` -> authoritative external state for grading;
6. `authorization_ledger()` -> hidden evaluator-side provenance of active grants and their scopes.

## Porting protocol

For each native benchmark task, construct matched siblings with the same goal and user preference evidence but different authorization timelines. Preserve the native environment and task success metric. Add GrantShift metrics: stale-authority execution, premature execution, repeated asking, update latency, and scope-transfer violations.

## Candidate environments

- Mobile/personal-assistant environments: map confirmations to concrete UI/tool actions.
- Coding agents: bind authorization to repository, file set, command class, or deployment target.
- Long-horizon office/tool environments: bind grants to connector, object, recipient, amount, or workflow version.

No external benchmark result is included in this release because downloading/running those environments and frontier agents requires external access. The adapter contract is provided so the missing experiment is explicit rather than hand-waved.
