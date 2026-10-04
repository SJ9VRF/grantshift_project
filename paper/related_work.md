# Related-work map

GrantShift should be reviewed as evaluation methodology, not as a claim to have invented proactive assistance.

| Work | Personalization | Proactivity | Consent/authorization | Long-term context | Real/interactive data | Matched preference-permission audit |
|---|---|---|---|---|---|---|
| Proactive Agent (ICLR 2025) | limited | yes | not central | limited | benchmark tasks | no |
| UserVille / PPP (2025) | yes | yes | not central | yes | SWE/browser tasks | no |
| ProAgentBench (2026) | context-aware | yes | not central | yes | 500+ hours real sessions | no |
| ProEvent (2026) | limited | yes | limited | event state | synthetic chats | no |
| KnowU-Bench (2026) | yes | yes | yes | interaction history | Android GUI | not primary design |
| Permission-policy work (2026) | user-authored policy | agent control | yes | policy context | human study | no |
| **GrantShift** | yes | yes | yes | history + drift | controlled pilot / planned external audit | **yes** |

## Positioning

The gap is not 'proactive agents need consent' - that is already established. The narrower contribution is a matched-counterfactual protocol for isolating how preference evidence changes intervention behavior under a fixed authorization boundary, coupled with burden and missed-opportunity metrics that make trivial safety policies visible.

The strongest publication validation is to transform tasks from interactive benchmarks such as KnowU-Bench and realistic-session benchmarks such as ProAgentBench into matched authorization counterfactuals, then test whether original benchmark scores hide permission failures.
