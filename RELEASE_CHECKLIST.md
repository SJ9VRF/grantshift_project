# Release Checklist

- [x] Deterministic benchmark generator
- [x] Deterministic stratified shuffled train/dev/test split
- [x] Separate contrastive personalization set
- [x] Schema validation
- [x] Heuristic baseline
- [x] Generic learned baseline
- [x] Personalized learned baseline
- [x] Held-out calibration
- [x] Pairwise preference/reward baseline
- [x] Preference-drift simulator
- [x] False-proactivity / missed-opportunity / autonomy metrics
- [x] Calibration metrics
- [x] Bootstrap confidence intervals
- [x] Per-domain regressions
- [x] Ablations
- [x] Failure taxonomy
- [x] Dataset card
- [x] Model card
- [x] Reproducibility guide
- [x] Decision trace
- [x] Human-eval UI prototype
- [x] Dashboard
- [x] Persisted calibrated policy bundle
- [x] Machine-readable CLI inference
- [x] Selective-intervention / restraint evaluation
- [x] Per-action confusion and severity diagnostics
- [x] Standalone offline interactive demo
- [x] Offline wheel build + clean-target install smoke test
- [x] Paper draft
- [x] Research talk
- [x] Demo script
- [x] Portfolio copy
- [x] Unit/regression tests
- [x] GitHub CI
- [x] OOD-domain evaluation
- [x] OOD-trigger evaluation
- [x] Leakage audit
- [x] Docker recipe
- [x] Verified dependency snapshot
- [x] Public research landing page
- [x] Dated prior-art / novelty audit
- [x] Non-colliding research name audit (not legal trademark clearance)
- [x] 240-case matched authorization-frontier set
- [x] Authorization-first personalized policy
- [x] Minimal-sufficient-action / overreach-distance metrics
- [x] Author metadata: Aura Yavary
- [x] Release audit
- [x] MIT license
- [ ] Human participant study — intentionally not fabricated
- [ ] External frontier-model/tool evaluation — requires provider/API access
- [ ] Real longitudinal deployment — requires consented users and production environment

## Project page release
- [x] Standalone `project/index.html` exists.
- [x] Hero exposes Paper / Code / Demo / Benchmark / Video.
- [x] All 14 requested sections are present.
- [x] Project-page local links are regression-tested.
- [x] Interactive trajectory uses actual release predictions.
- [x] Paper PDF exists and was render-verified.
- [x] Video walkthrough exists and is playable MP4.
- [x] Engineering report, blog post, and BibTeX citation are included.
- [x] Scaling block uses measured latency and explicitly states tool-count / deployment limits.

## v0.9.0 project-page completeness audit

- [x] Hero: project name, clear problem statement, headline result, Paper / Code / Demo / Benchmark / Video CTAs
- [x] 60-second summary: problem / contribution / result / evidence scope
- [x] Why this problem matters
- [x] Core idea and bounded novelty statement
- [x] Architecture: main system + agent loop + real preference-learning/recovery/training loops (no fabricated online-RL claim)
- [x] My contribution: design / implementation / technical decisions
- [x] Experiments: dataset/tasks / baselines / ablations / setup
- [x] Results: baseline → method plus success / recovery / latency / cost table
- [x] Failure analysis: real failures, causes, recovery path
- [x] Interactive trajectory demo
- [x] Scaling: model size / horizon / tool count / cost-latency / robustness
- [x] Safety / limitations: failure regions / irreversible actions / permission boundaries / human escalation
- [x] Technical deep dive: engineering report / training details / evaluation methodology
- [x] Artifacts: Paper / GitHub-ready Code / Benchmark / Dataset / Demo / Video / Technical report / Blog post
- [x] Citation: BibTeX / Aura Yavary / 2026


## v1.4.0 submission hardening
- [x] 6,000-case grouped factorial inputs regenerated from contextual natural-language evidence.
- [x] 900-case held-out paraphrase stress test executed.
- [x] Utility-sensitivity grid executed.
- [x] Public and anonymous LaTeX PDFs reproduced from source.
- [x] Anonymous PDF checked for author-name leakage.
- [x] Exact experiment config and compute disclosure included.
- [x] Reviewer checklist and rebuttal notes included.
- [x] Clean wheel 1.4.0 built and installed in an empty target.
- [x] Anonymous submission source bundle audited.
- [x] Full test suite and release audit passed.

## v1.4.0 agent-eval and post-training hardening

- [x] Stateful multi-turn evaluation harness implemented.
- [x] 144 agent tasks exported across six domains.
- [x] 2,880 repeated trials executed and persisted.
- [x] Final environment state verified separately from transcript claims.
- [x] Authorization, outcome, interaction-efficiency, and recovery graders implemented.
- [x] pass@k and pass^k reliability reported.
- [x] Irreversible ask-required recovery corrected to defer/escalate after confirmation rather than force ACT.
- [x] Capability and regression task manifests exported.
- [x] Failed trajectories mined into incident bank.
- [x] Incidents prioritized by severity/frequency and converted into weighted training pairs.
- [x] Human/model-grader calibration utility added without fabricating calibration results.
- [x] Paper and homepage updated with bounded trajectory-level claims.
- [x] Clean wheel 1.4.0 built and installed in an empty target.
- [x] Public and anonymous PDF rebuilt and anonymous source audited.

## v1.4.0 state-tracking and evidence hardening

- [x] Added delayed-confirmation, permission-revocation, and transient-tool-failure environment variants.
- [x] Added `RobustAuthorizationAgent` and explicit state-tracking grader.
- [x] Executed 90-task / 1,350-trial cross-environment suite.
- [x] Added 11 grader-rubric regression cases; all match expected labels.
- [x] Added machine-readable claim-to-evidence registry and audit.
- [x] Added environment-shift paper section, figure, and reviewer dossier.
- [ ] Human participant study executed.
- [ ] Frontier-model evaluation executed.
- [ ] External interactive benchmark audit executed.
