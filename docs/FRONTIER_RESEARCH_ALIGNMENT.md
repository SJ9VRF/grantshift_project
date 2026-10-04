# Research-engineering alignment

This file documents why the v1.3 milestone added trajectory evaluation and a failure-to-training loop. It is not a hiring claim and does not replace empirical evidence.

Current OpenAI agent post-training roles emphasize end-to-end ownership of RL/post-training stacks, data pipelines, graders, reward signals, evals, diagnostics, failure mining, training data, reproducibility, latency, cost, and production-like environments. OpenAI's Personal AGI roles also emphasize personalization, proactivity, memory, evaluations, and post-training.

Anthropic's January 2026 agent-evaluation guidance formalizes tasks, trials, graders, trajectories, outcomes, evaluation harnesses, multiple grader types, and repeated-trial reliability. It also emphasizes state verification rather than trusting a model's completion claim.

GrantShift v1.3 therefore adds the missing mechanics that are possible to execute locally: multi-turn state mutation, trajectory capture, outcome verification, repeated trials, pass@k/pass^k summaries, incident mining, and training-pair export. It still does not claim real frontier-model post-training or production-environment safety.

Public references:
- https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- https://openai.com/careers/agent-post-training-connectors-research-san-francisco/
- https://openai.com/careers/research-engineer-frontier-evals-and-environments-san-francisco/
- https://openai.com/careers/research-engineer-research-scientist-personal-agi-personalization-san-francisco/
