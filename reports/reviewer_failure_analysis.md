# Reviewer-style failure analysis

## Strongest skeptical reading

**Objection 1: “This is a hand-written policy benchmark, not an AI result.”**  
Correct for the current mechanism experiments. The synthetic policies validate the measurement instrument; they do not establish frontier-model performance. The paper should be rejected if it presents 100% state-machine accuracy as a model result.

**Objection 2: “Permission and consent benchmarks already exist.”**  
Correct. The novelty claim is intentionally narrower: fixed preference evidence + controlled dynamic authorization transitions + scope/version binding + trajectory-level stale-authority metrics. The paper must cite KnowU-Bench, changing-world personalization benchmarks, overreach benchmarks, and revocation work prominently.

**Objection 3: “Latest-state policy already solves the transition suite.”**  
This was a real weakness in v1.0. The scope-bound adversarial suite was added specifically to falsify the idea that reading the most recent authorization label is sufficient. It creates delayed or stale grants tied to an obsolete action scope.

**Objection 4: “Synthetic language may leak the answer.”**  
Yes. The release includes paraphrase stress tests, evidence shuffles/masking, and explicitly labels all synthetic results as mechanism checks. Frontier-model and human experiments remain required.

**Objection 5: “The oracle is normative.”**  
Only in controlled synthetic cases where authorization semantics are constructed by design. For ambiguous real-world cases, acceptable-action sets must come from participant labels or policy owners. The human-study protocol keeps individual judgments rather than collapsing disagreement prematurely.

**Objection 6: “Why not enforce permissions deterministically outside the model?”**  
For high-consequence actions, deterministic capability/authorization enforcement is desirable. GrantShift targets the behavioral and harness layer: whether an agent requests, waits, interprets, and updates authority correctly before an enforcement boundary is reached. It is complementary to capability systems, not a substitute.

## Submission-changing experiments still missing
1. contemporary frontier agents under the same matched transitions;
2. multiple harnesses to separate model behavior from scaffold behavior;
3. human authorization labels for ambiguous cases;
4. one external realistic environment;
5. model-level mitigation or post-training A/B, not only a hand-coded state machine.
