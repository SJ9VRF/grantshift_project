# GrantShiftBench Dataset Card

## Purpose
Controlled evaluation of grantshift-agent judgment across intervention type, risk, uncertainty, autonomy preference, and temporal urgency.

## Contents
- 600 deterministic synthetic scenarios in `scenarios/v1.jsonl`
- 160 contrastive personalization scenarios in `scenarios/contrast_v1.jsonl`
- 240 matched intervention-frontier scenarios (60 base states × four authorization modes) in `scenarios/frontier_v1.jsonl`
- deterministic stratified train/dev/test IDs plus explicit OOD-domain and OOD-trigger protocols
- five reusable user profiles
- multi-valid acceptable actions, explicit bad actions, and wrong-action severity

## Domains
Productivity, career, travel, communication, calendar, shopping, routines, privacy, financial, information, social, and high-stakes tasks.

## Intended use
Research prototyping, regression tests, ablations, calibration experiments, reward-model experiments, and demonstration of evaluation infrastructure.

## Not intended for
Claims about real users, deployment thresholds, psychological inference, or population-level preference conclusions.

## Limitations
Labels come from a transparent synthetic oracle. Synthetic consistency is not human validity. Natural-language diversity and real-world tool outcomes are intentionally limited in v1.

## Intervention-frontier fields

Frontier cases add explicit `authorization` (`advisory`, `ask_required`, `preauthorized`, `prohibited`) and `recoverable` metadata. The matched set varies authorization while holding the base opportunity approximately fixed. Frontier metrics include minimal-sufficient-action rate, mean overreach distance, authorization violations, and irreversible autonomous acts.

**Author:** Aura Yavary

## v2 natural-language factorial pilot

Version 1.0.0 includes `grantshiftbench/v2/factorial_inputs.jsonl` and a separate `factorial_gold.jsonl`.
The evaluated input contains natural-language history, a standing instruction, the current situation, and the action set. Structured latent preference, authorization, stakes, reversibility, urgency, and labels are kept in the gold file for analysis only. All counterfactual siblings from a base situation remain in one split.

Scale: 500 base situations × 3 preference histories × 4 authorization conditions = 6,000 cases.

This remains synthetic data. It is intended for mechanism testing, evaluator development, and human-study preparation—not as a substitute for human judgment or real-agent interaction data. Croissant metadata is provided in `grantshiftbench/croissant.json`.


## Surface-form stress set
Version 1.0.0 adds `factorial_paraphrase_test_inputs.jsonl`, a second natural-language realization of the 900 held-out factorial cases. It is designed to expose template sensitivity; it does not add new human labels.

## Robustness suite (1.0.0)

The release includes authorization/preference evidence corruption controls, five train-base subsample fits, leave-one-domain-out evaluation, and train-only surface augmentation. These operate on synthetic labels and are intended to diagnose shortcuts, not establish population-level behavior.

## Scope-bound authorization stress test (1.2.0)

`grantshiftbench/adversarial/scope_bound_transitions.jsonl` adds 1,080 trajectories in which authorization is bound to a task scope/version. The suite includes material scope changes, delayed confirmation for obsolete scopes, revocation/regrant, expiration/refresh, double supersession, and new requests after denial. Gold actions are synthetic by construction and should not be treated as human normative labels.
