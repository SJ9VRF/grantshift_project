# GrantShift: Stress-Testing Dynamic Authorization in Personalized AI Agents

**Aura Yavary**

## Abstract

Personalized AI agents must distinguish what a user tends to want from what the agent is allowed to do now. GrantShift treats authorization as a **time-varying, scope-bound state** rather than a static permission label. The primary transition suite contains 1,260 controlled trajectories across six personal-assistant domains, three fixed preference histories, and seven transition families: grant, delayed confirmation, denial, revocation, expiration, supersession, and stale-confirmation invalidation. A second 1,080-trajectory adversarial suite binds grants to action scope/version, and an 864-trajectory provenance challenge binds grants to principal/request/resource/revision/nonce so that delayed or stale grants cannot safely transfer to a materially changed action. In deterministic synthetic mechanism checks, a static-initial-authority policy reaches 47.1% exact transition compliance with 11.8% stale-authority execution. A latest-authorization-label policy reaches 100% on the easier suite but falls to 88.9% exact with 11.1% stale-scope execution on the adversarial suite; an explicit scope-aware state machine remains exact. Cluster-bootstrap uncertainty and paired exact tests are included, but these numbers validate the instrument rather than frontier-model performance. The release also contains a 6,000-case preference-by-authorization audit, a 900-case paraphrase stress test, trajectory-level environment verification, incident mining, human-study infrastructure, and provider-neutral frontier-model scoring. No human-validity or frontier-model SOTA claim is made without external data.

## 1. Introduction

A useful personal agent should know the user. A trustworthy personal agent should also know the limits of that knowledge.

Suppose a user often asks an assistant to handle routine calendar changes automatically. Later, the assistant encounters a socially sensitive meeting, a costly travel change, or an operation the user has explicitly restricted. The user's history is relevant, but it is not equivalent to authorization. A system that collapses these two signals may become *more personalized and more intrusive at the same time*.

This distinction matters because proactive-agent evaluation is commonly organized around task success, timing, intent prediction, preference recovery, or generic intervention quality. Recent benchmarks expand substantially toward realistic user context and interactive personalization, but preference alignment and permission compliance remain easy to aggregate into a single notion of helpfulness. GrantShift instead treats them as separate axes.

We study the **preference-permission gap**:

> When authorization is held fixed, how much can preference evidence change an agent's willingness to take an action that exceeds the user's current permission boundary?

The paper is designed as an evaluation-methodology contribution rather than a leaderboard paper. Its core artifact is a matched-counterfactual protocol that manipulates preference evidence and authorization independently, measures both helpfulness and control costs, and makes trivial safety strategies such as `always ask` visible through interaction-burden metrics.

### Contributions

1. **Problem formulation.** We distinguish persistent preference from task-specific authorization and define the preference-permission gap as a measurable behavioral failure mode.
2. **Counterfactual evaluation protocol.** We construct matched variants that independently manipulate preference history and authorization while grouping siblings at the base-scenario level to prevent train/test leakage.
3. **Natural-language factorial pilot.** We release 6,000 blinded inputs (500 base situations × 3 preference histories × 4 authorization conditions) with private synthetic gold and latent factors separated from evaluated inputs.
4. **Evaluation beyond accuracy.** We report unauthorized autonomous action, question burden, unnecessary intervention, missed opportunity, expected utility sensitivity, and longitudinal regret in addition to exact and acceptable action match.
5. **Publication-grade infrastructure.** We provide a human-study protocol, provider-neutral frontier-model prompt/scoring harness, consequence simulator, long-horizon drift environment, power analysis, Croissant metadata, and deterministic release tooling.
6. **Bounded claims.** We explicitly separate synthetic mechanism evidence from human or frontier-model evidence. No human-study or external-model result is fabricated in this release.

## Authorization transitions (GrantShiftBench-Transitions)

The new core benchmark contains 1,260 controlled trajectories across six domains, three fixed preference histories, and seven authorization transition families: grant, delayed confirmation, denial, revocation, expiration, supersession, and stale-confirmation invalidation. Preference is deliberately held fixed while authority changes. Primary metrics are stale-authority execution, premature execution, repeated confirmation, and authorization-update latency.

Synthetic mechanism check: static initial authority reaches 47.1% exact compliance with 11.8% stale-authority execution; the explicit state-machine policy reaches 100% exact compliance with 0% stale-authority execution and zero-step update latency. These are instrument checks, not frontier-model results.

### Scope-bound adversarial authorization

The base suite can be solved by consuming the latest authorization label. GrantShift v1.2 therefore adds **1,080 adversarial trajectories (3,240 steps)** where grants are bound to an action scope/version. When task parameters change or a confirmation arrives late for an obsolete scope, a policy must verify grant provenance rather than transfer permission automatically. A latest-label policy scores 88.9% exact with 11.1% stale-scope execution; the scope-aware state machine is exact in the deterministic mechanism test. A trajectory-cluster bootstrap gives a 95% CI of 88.0-89.8% exact for the latest-label policy, and the paired exact comparison has 360 discordant steps, all favoring scope-aware tracking ($p<10^{-108}$). These statistics quantify the synthetic benchmark, not a population of users or frontier models.

## 2. Related Work and Positioning

Proactive-agent work has moved from reactive response generation toward timing, intent anticipation, and continuous assistance. Proactive Agent introduced a benchmark and training setup for active assistance. UserVille/PPP combines proactive and personalized agent training. ProAgentBench emphasizes long-term real user context and reports that real-session data differs materially from synthetic alternatives. ProEvent evaluates event-centric proactive behavior and reports over-action and event-cancellation failures. KnowU-Bench evaluates interactive, proactive, personalized mobile agents in a GUI setting, including preference elicitation, intervention, consent seeking, and silence.

GrantShift is deliberately narrower. It does not claim to replace end-to-end proactive-agent benchmarks. It asks whether those systems preserve a distinction between **what the user tends to want** and **what the agent is authorized to do in the present context**, and supplies a controlled counterfactual protocol for auditing that distinction.

| Work | Personalization | Proactivity | Explicit authorization/consent | Matched preference × permission counterfactuals | Real/interactive environment |
|---|---:|---:|---:|---:|---:|
| Proactive Agent | limited | yes | limited | no | benchmark tasks |
| UserVille / PPP | yes | yes | not central | no | SWE/browser tasks |
| ProAgentBench | context-aware | yes | not central | no | real user-session data |
| ProEvent | limited | yes | limited | no | event-centric chats |
| KnowU-Bench | yes | yes | yes | not the primary design | Android GUI |
| **GrantShift** | yes | yes | **yes** | **yes** | controlled mechanism benchmark + simulator |

The strongest external validation for GrantShift would be to apply its counterfactual audit protocol to tasks drawn from interactive benchmarks such as KnowU-Bench and realistic session data such as ProAgentBench. The current release prepares that evaluation but does not claim it has already been run.

## 3. Preference and Permission Are Different Variables

Let `s` denote the current task state, `h_u` the user's historical behavior and preferences, and `z` the authorization state governing the present action. An intervention policy selects

`a ~ pi(a | s, h_u, z)`

from

`A = {ACT, ASK, SUGGEST, REMIND, WAIT, DEFER, DO_NOTHING}`.

Preference evidence changes the utility of candidate actions; authorization changes the feasible or acceptable action set. GrantShift therefore treats authorization as a constraint rather than a synonym for preference strength.

We define three quantities.

### 3.1 Preference alignment

The degree to which the chosen action matches an individual's stated or behaviorally inferred intervention preference.

### 3.2 Permission compliance

Whether the action remains inside the present authorization boundary. Autonomous execution outside a preauthorized boundary is counted separately from a merely suboptimal suggestion.

### 3.3 Preference-permission gap

For fixed state and fixed authorization, let `O(pref)` be the autonomous-overreach rate under a preference condition. The gap is the change in overreach attributable to preference evidence:

`PPG(auth; p1, p2) = O(auth, p1) - O(auth, p2)`.

A non-zero gap under a fixed authorization boundary indicates that preference evidence is influencing whether the model crosses that boundary.

## 4. GrantShift Factorial Protocol

### 4.1 Counterfactual design

The v2 pilot contains 500 base situations across email, calendar, travel, shopping, files, communication, and productivity. Each base situation is crossed with three preference histories and four task-specific authorization conditions, yielding 6,000 natural-language cases.

Preference histories:
- **autonomous:** the user has repeatedly welcomed low-risk automatic handling;
- **confirmation-seeking:** the user has corrected unauthorized changes and prefers confirmation;
- **minimal-interruption:** the user has muted low-value reminders and prefers silence.

Authorization conditions:
- **prohibited:** do not act or contact the user about the task unless asked;
- **ask-required:** obtain confirmation before action;
- **advisory:** suggestions are allowed but execution is not;
- **preauthorized:** reversible, low-risk execution is allowed.

The same base situation also varies stakes, reversibility, and urgency. These latent factors are stored in the private gold file for analysis but are **not exposed as structured fields in the evaluated input**. The model sees a natural-language situation, short interaction history, standing instruction, and available action set.

### 4.2 Grouped split

All 12 preference × authorization siblings from a base situation remain in the same split. The deterministic split is 70% train, 15% development, and 15% test at the base-situation level. This prevents a model from training on one counterfactual sibling and being evaluated on another nearly identical sibling.

### 4.3 Synthetic pilot labels

The current gold labels are generated by a latent policy over preference, authorization, stakes, reversibility, and urgency. The policy is used only to test evaluation machinery. Because the labels are author-designed, they do not establish human normative validity. The publication-grade protocol replaces these labels with blinded participant judgments and preserves the same counterfactual structure.

## 5. Metrics

Exact action accuracy alone is insufficient because `ASK` can be safe yet burdensome, while `ACT` can be useful yet unauthorized.

We report:
- **Exact action match.** Chosen action equals preferred action.
- **Acceptable action rate.** Chosen action belongs to a human- or oracle-provided acceptable set.
- **Unauthorized autonomous action rate.** `ACT` occurs outside preauthorization.
- **Question burden.** Fraction of cases in which the agent asks.
- **Unnecessary intervention rate.** The agent intervenes when non-intervention is preferred.
- **Missed opportunity rate.** The agent stays silent when intervention is preferred.
- **Expected intervention utility.** A sensitivity-testable objective that penalizes unauthorized actions, interruptions, questions, and missed opportunities.
- **Longitudinal regret and adaptation latency.** Used after preference drift.

Utility weights are explicitly configurable and are not treated as universal human values.

## 6. Controlled Pilot Experiments

### 6.1 Conditions

We train the same TF-IDF + multinomial logistic-regression sanity baseline under four information conditions:

- **C0 State only:** task situation, no preference or authorization evidence.
- **C1 State + preference:** task situation plus user-history evidence.
- **C2 State + authorization:** task situation plus standing authorization instruction.
- **C3 Full:** state + preference history + authorization.

These are not proposed as state-of-the-art agents. They test whether the evaluation protocol detects the intended causal structure before expensive model evaluation.

### 6.2 Main pilot results

| Condition | Exact | Acceptable | Unauthorized ACT | Question burden | Synthetic utility |
|---|---:|---:|---:|---:|---:|
| C0 state only | 21.9% | 38.6% | **35.0%** | 9.3% | -1.109 |
| C1 + preference | 36.4% | 55.2% | **14.6%** | 23.7% | -0.441 |
| C2 + authorization | 90.1% | 90.1% | **0.0%** | 38.3% | 0.657 |
| C3 full | **98.7%** | **98.7%** | **0.0%** | 39.2% | **0.734** |
| Always ask | 42.2% | 69.0% | 0.0% | **100%** | -0.025 |
| Always silent | 31.0% | 31.0% | 0.0% | 0.0% | -0.898 |
| Always act | 5.0% | 5.0% | **75.0%** | 0.0% | -2.456 |

Three mechanism checks emerge. First, task state alone is insufficient to infer permission. Second, preference evidence helps but does not eliminate unauthorized action. Third, explicit authorization is the dominant control signal in this synthetic pilot, while preference evidence supplies a smaller gain within the authorized envelope. The `always ask` baseline demonstrates that eliminating autonomous overreach by universal confirmation produces maximal interaction burden and poor utility under the pilot weights.

These results validate the *evaluation design*, not a claim about real users or frontier LLMs.

## 7. Long-Horizon Preference Drift

We include a 100-turn simulator in which a user's intervention preference changes at turn 40. A frozen profile mismatches every post-drift decision in the constructed trajectory. An adaptive profile that updates only after observed correction recovers after one turn in the deterministic seed used by the release and has 1.7% post-drift mismatch. This is an executable stress test of stale-profile handling, not a substitute for a longitudinal user study.

The publication protocol will measure adaptation latency, stale-action count, cumulative regret, correction burden, and overreach after drift with real users.

## 8. Consequences and Irreversibility

GrantShift includes a small consequence simulator for email, calendar, travel, shopping, and file operations. Autonomous execution can create monetary, privacy, social, or irreversibility costs; asking and suggesting preserve reversibility but delay task completion. The simulator exists to ensure that `ACT` is not merely a text label in downstream experiments and to support future sequential-policy work.

A publication-grade interactive evaluation should replace these stylized consequences with sandboxed real tools or benchmark environments.

## 9. Human Validation Protocol

The human study is preregistration-ready but has **not been run** in this release. Participants receive blinded, randomized counterfactual scenarios and select a preferred action plus an acceptable-action set. They rate appropriateness, helpfulness, perceived control, annoyance, and overreach. The primary analysis uses mixed-effects models with participant and base-scenario random effects. We report inter-annotator agreement, label entropy, individual-level labels, and consensus labels separately.

Power-analysis tooling is included. The default script uses a conservative normal approximation for planning and explicitly instructs authors to replace it with pilot-informed mixed-effects simulation before preregistration.

## 10. Frontier-Model Evaluation Protocol

The repository exports 6,000 factorial prompts plus 6,300 transition/scope prompts without gold labels and provides provider-neutral scorers. A complete paper should evaluate multiple contemporary model families under the four C0-C3 information conditions and report model-scale, reasoning, and prompting sensitivity. No external-model numbers appear in this release because no provider outputs were available during construction.

The key empirical test is not whether a frontier model can reproduce the synthetic oracle. It is whether adding richer personalization evidence changes permission overreach under human-validated authorization boundaries.

## 11. External-Benchmark Audit

GrantShift is best positioned as an **evaluation audit** rather than a replacement for existing proactive-agent benchmarks. We propose applying the matched preference × permission transformation to tasks sampled from interactive or realistic benchmarks, where licensing allows. If a model performs well on the original benchmark but fails under counterfactual authorization changes, GrantShift reveals a behavior hidden by the aggregate score.

This external audit is a required publication experiment and is not represented as completed here.

## 12. Reproducibility and Dataset Governance

The release contains deterministic generators, grouped splits, machine-readable metrics, CI tests, a source distribution, a release audit, and Croissant metadata. The benchmark card documents synthetic provenance, intended use, out-of-scope use, and known biases. The release includes separate files for blinded inputs and gold/latent annotations so that model evaluation can be performed without accidental label exposure.

## 13. Limitations

The main limitation is decisive: all quantitative results in this release are synthetic mechanism checks. They do not establish human preferences, trust, safety, or frontier-agent performance. The natural-language generator remains templated. Utility weights are design parameters. The consequence environment is stylized. No prospective deployment, IRB-reviewed participant study, external LLM evaluation, or real-tool benchmark audit has been executed.

Accordingly, the strongest supported claim is methodological: **preference evidence and permission evidence should be manipulated and evaluated separately**. The stronger empirical claim - that contemporary personalized agents systematically overreach because they confuse the two - remains a hypothesis until validated on humans and external models.

## 14. Conclusion

Personalization answers “what does this user tend to want?” Permission answers “what may the agent do now?” Treating these as one variable creates a blind spot in proactive-agent evaluation. GrantShift provides a controlled way to expose that blind spot, measure the usefulness-control trade-off, and test whether richer personalization causes permission leakage. The current release establishes the methodology and reproduces its intended causal behavior in a synthetic natural-language pilot. The next scientific step is deliberately empirical: human validation, frontier-model evaluation, and audit of realistic proactive-agent benchmarks.


## Surface-form stress test

On a 900-case held-out paraphrase realization of the same test base states, the full classical baseline falls to **52.8% exact / 76.2% acceptable** and asks on **86.1%** of cases, while unauthorized ACT remains 0%. This negative result shows substantial template sensitivity and is a central limitation of the synthetic pilot.

## Trajectory-level agent evaluation (v1.3)

The release now includes a stateful multi-turn sandbox with 144 tasks across six domains, five trials per task/policy, full trajectory logging, final-state verification, and separate authorization/outcome/efficiency/recovery graders. The executed run contains 2,880 trials. A deterministic authorization-first policy solves the controlled sandbox, while an 8% seeded action-noise wrapper reaches 96.5% trial success but only about 83.8% all-five-trials consistency. The run also mines 1,142 failed trials into an incident bank and exports the same number of weighted chosen/rejected records for downstream post-training experiments. These are sandbox mechanics, not frontier-agent results.
