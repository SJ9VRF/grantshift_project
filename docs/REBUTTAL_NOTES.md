# Likely reviewer questions and evidence locations

**Is the benchmark just recovering its own rule?**  
The release explicitly treats v2 as a synthetic mechanism check. Structured latent factors are withheld from inputs, counterfactual siblings are group-split, and a held-out paraphrase stress test drops exact match from 98.7% to 52.8%, demonstrating that the classical text baseline still relies heavily on surface regularities. The paper presents this as a limitation, not as a model achievement.

**Why not always ask?**  
Always-ask has zero unauthorized ACT but 100% question burden and lower synthetic utility. The release includes a utility-sensitivity grid rather than relying on a single confirmation cost.

**Is exact action match meaningful?**  
It is secondary. The framework separately reports authorization violations, burden, missed opportunity, unnecessary intervention, and acceptable-action sets. Human validation is required before treating the synthetic preferred action as normative.

**How is GrantShift different from KnowU-Bench or ProAgentBench?**  
Those benchmarks test broader end-to-end proactive/personalized behavior. GrantShift isolates a narrower causal question: how preference evidence changes intervention behavior while authorization is held fixed. The strongest future validation is to apply this audit protocol to tasks from those environments.

**Does this show frontier LLMs overreach?**  
No. The release includes blinded prompts and a provider-neutral scoring harness, but no external model outputs are fabricated.
