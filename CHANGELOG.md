# Changelog

## 1.7.0 — Evidence integrity and clean-room release audit
- Rebuilt from the complete v1.6 release archive after detecting that a separately materialized folder was incomplete.
- Added machine-readable claim → experiment → raw-artifact evidence graph and reviewer-facing HTML graph.
- Added a skeptical reviewer red-team that explicitly separates supported mechanism claims from unsupported frontier/human/production claims.
- Added one-command core reproduction with command outcomes and SHA-256 hashes.
- Added a public-number consistency gate across homepage, README, and executed eval tables.
- Added Exp-014 documenting failure-to-training-data infrastructure without claiming model improvement.
- Added release tests for evidence-graph completeness and consistency-gate readiness.


## 1.4.0 - Scope-bound authorization hardening

- Added 1,080 adversarial scope/version-bound authorization trajectories.
- Added trajectory-cluster bootstrap confidence intervals and paired exact tests.
- Added provider-neutral transition prompt export/scoring for frontier-model runs.
- Added claim-to-ablation matrix, external-environment adapter spec, reviewer failure analysis, and hiring-manager brief.
- Added tests that prevent a latest-label policy from being mistaken for a scope-aware authorization mechanism.
# Changelog

## 1.4.0 - 2026-09-25

- Added cross-environment trajectory stress tests for delayed confirmation, permission revocation, and transient tool failure.
- Added a state-tracking authorization policy and a dedicated state-tracking grader.
- Added grader-rubric regression cases and machine-readable claim-to-evidence gating.
- Added cross-environment results, claim evidence audit, and regression tests.
- Updated package, paper, source bundle, and anonymous submission metadata to 1.4.0.


## 1.4.0 - 2026-09-25

- Added trajectory-level agent evaluation with tasks, repeated trials, graders, trajectories, and verified end states.
- Added pass@k/pass^k reliability, recovery grading, capability/regression manifests, incident mining, prioritization, and failure-derived training-pair export.
- Added grader-calibration tooling and documentation for the failure-to-training flywheel.
- Extended the paper with trajectory reliability and post-training-loop evidence.
- Updated package/submission/release metadata to 1.4.0.

## 1.4.0 - 2026-09-25
- Added v2 evidence-channel negative controls.
- Added train-subsample robustness and leave-one-domain-out evaluation.
- Added deterministic surface augmentation mitigation and paper figures.
- Updated public/anonymous submission tooling and package metadata to 1.4.0.

## 1.4.0 - 2026-09-24
- Replaced explicit scalar words in v2 inputs with contextual natural-language consequences.
- Added held-out paraphrase stress test and surface-generalization artifact.
- Added utility-weight sensitivity analysis.
- Added public + anonymous LaTeX submission sources and figures.
- Added exact submission config, compute disclosure, reviewer checklist, rebuttal notes, reproduction script, and anonymous submission builder.
- Bounded claims around the 52.8% paraphrase exact-match failure.


## 1.4.0 — Editorial cleanup

- rewrote the project page and README to remove template-like and presentation-directed language;
- removed duplicated result copy and synchronized the documented test count;
- renamed the internal project-summary note and kept release metadata/versioning consistent;
- rebuilt package, source bundle, manifests, and release checks from the cleaned tree.

# v1.4.0 — Project-page completeness hardening

- Audited the project page against all 14 requested sections.
- Added a 60-second hiring-manager summary.
- Added explicit agent / recovery / training loops without fabricating online RL.
- Added success / recovery / latency / external-cost results table.
- Added an independent GitHub-ready source bundle and publication note.
- Extended release audit and regression tests to enforce project-page completeness.

# Changelog

## 1.4.0 - 2026-09-25

- Added trajectory-level agent evaluation with tasks, repeated trials, graders, trajectories, and verified end states.
- Added pass@k/pass^k reliability, recovery grading, capability/regression manifests, incident mining, prioritization, and failure-derived training-pair export.
- Added grader-calibration tooling and documentation for the failure-to-training flywheel.
- Extended the paper with trajectory reliability and post-training-loop evidence.
- Updated package/submission/release metadata to 1.4.0.

## 1.4.0 — 2026-09-23

- Added a standalone, publication-quality project homepage at `project/index.html` with the complete 14-part hiring-manager narrative: hero, problem, core idea, architecture, contribution, experiments, results, failures, interactive trajectory, scaling, safety, technical deep dive, artifacts, and citation.
- Added a project video walkthrough (`project/assets/grantshift-overview.mp4`).
- Added a rendered research-paper PDF (`paper/grantshift-paper.pdf`) and verified the PDF by rendering it to images.
- Added `docs/engineering_report.md`, `docs/blog_post.md`, and `CITATION.bib`.
- Added measured local inference latency to the project page: 3.4 ms p50 / 4.0 ms p95 across 2,000 local CPU decisions.
- Added release-audit and regression checks for the project-page artifact bundle.

## 0.6.0 — 2026-09-23
- Added paired-bootstrap accuracy deltas and exact McNemar tests.
- Added matched-group authorization counterfactual metrics.
- Added generic authorization-gated baseline for a fair constraint ablation.
- Added probability-masked constrained intervention ranker.
- Added local numeric-jitter sensitivity evaluation.
- Added benchmark provenance hashes and generator/split manifest.
- Expanded tests from 23 to 25 and tightened release audit requirements.
- Revised paper claims to distinguish preference personalization from permission robustness and to expose the accuracy–restraint tradeoff.

## 0.5.0
- Renamed project to GrantShift / GrantShiftBench after prior-art and name-collision audit.
- Reframed research contribution as a personalized intervention frontier.
- Added authorization and recoverability to state features.
- Added a 240-case matched authorization frontier benchmark.
- Added authorization-first personalized policy and frontier-specific metrics.
- Added novelty audit, related-work notes, references, and Aura Yavary author metadata.
- Added v0.5.0 package/wheel smoke validation.

## 0.4.0
- Replaced generator-order train/dev/test assignment with deterministic stratified shuffled splits.
- Added OOD-domain and OOD-trigger evaluation protocols.
- Added explicit input-leakage audit and regression tests.
- Added container recipe and verified-environment dependency snapshot.
- Expanded release documentation around synthetic-oracle limits and generalization failures.
- Added a self-contained public research-release landing page.

## 0.3.0
- Added deployable model bundle, CLI, offline wheel smoke test, selective-intervention evaluation, action diagnostics, and interactive demo.

## 0.2.0
- Added held-out calibration, statistical uncertainty, domain metrics, CI, dataset/model cards, and release audit.

## 0.1.0
- Initial benchmark, heuristic and learned policies, personalization contrast set, drift simulator, dashboard, and paper draft.

## 1.4.0 - Evaluation-paper rebuild
- Reframed GrantShift around the preference-permission gap rather than a generic proactive-agent claim.
- Added 6,000-case natural-language factorial benchmark with base-grouped counterfactual splits.
- Separated blinded model inputs from synthetic gold/latent analysis factors.
- Added C0-C3 information ablations and always-ask/silent/act/suggest baselines.
- Added intervention burden, unauthorized-action, missed-opportunity and configurable utility metrics.
- Added a 100-turn drift simulator and stylized consequence environment.
- Added preregistration-ready human-study protocol, annotation schema and power-analysis tooling.
- Added provider-neutral frontier-model prompt export/scoring harness.
- Added Croissant metadata and explicit empirical-status documentation.
- Rewrote the paper around bounded methodological claims and removed stale structured-pilot headline claims.

## 1.6.0 — Evidence Layer
- Added artifact-backed experiment journal, failed-experiment record, decision log, real eval tables, and unexpected findings.
- Added raw evidence directory structure for eval runs, failures, configs, qualitative cases, and ablations.
- Added honest Git-history policy and began incremental commits from an explicitly labeled v1.5.0 import snapshot.
- Added `Inside the research process` layer to the flagship homepage.
