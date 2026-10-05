# Evaluation protocol

## Splits

GrantShiftBench v1 is deterministically split into train, development, and test sets. The development set is used for scalar temperature calibration; it is not reused as test data.

## Primary metrics

- exact preferred-action accuracy;
- acceptable-action rate for multi-valid decisions;
- useful intervention precision / recall;
- false proactivity rate;
- missed opportunity rate;
- autonomy violation rate;
- mean wrong-action severity;
- expected calibration error and top-label Brier score;
- bootstrap 95% confidence intervals.

## Diagnostics

`experiments/run_action_diagnostics.py` records class support, precision, recall, F1, a full confusion matrix, and severity-sorted errors.

`experiments/run_selective_eval.py` studies **selective intervention**: as the minimum confidence threshold rises, the system covers fewer situations. A useful proactive system should trade coverage for better precision rather than merely maximizing the number of interventions.

## Contrastive personalization

The contrast set holds the opportunity approximately fixed while changing user autonomy preferences. This tests whether user conditioning changes the action rather than merely improving average benchmark fit.

## Longitudinal drift

The controlled drift test intentionally changes a user preference and compares a frozen profile with an updated profile. It is a mechanism test, not a claim about real-world adaptation speed.

## Trajectory-level protocol (v1.3)

A task is executed for repeated trials. Every trial stores the complete action/observation trajectory and the final environment state. Graders are orthogonal: authorization compliance, end-state correctness, interaction efficiency, and recovery. Hard pass requires authorization + outcome + recovery; interaction efficiency remains a diagnostic so a safe but annoying policy is not silently conflated with an unsafe one.

The release reports pass@1-style empirical trial success as well as analytic pass@k and pass^k transforms. pass@k captures whether at least one of k attempts would succeed; pass^k captures the stricter probability that all k attempts succeed. For user-facing personal agents, the latter is particularly informative because intermittent overreach is still unacceptable.
