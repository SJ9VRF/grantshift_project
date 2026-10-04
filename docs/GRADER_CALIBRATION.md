# Grader calibration

GrantShift uses deterministic graders for the executable sandbox because authorization and final-state mutation are directly inspectable. Subjective dimensions such as appropriateness, tone, and perceived control require model- or human-based graders in an external study.

`evaluation/grader_calibration.py` provides binary agreement metrics (accuracy, precision, recall, F1, Cohen's kappa) for calibrating a candidate automated grader against a human reference sample. The intended workflow is:

1. draw a stratified sample across authorization states and domains;
2. obtain blinded human judgments;
3. run the candidate model grader on the same items;
4. compute agreement and inspect disagreement slices;
5. revise the rubric if systematic bias remains;
6. only then scale the automated grader to the full evaluation set.

No human-calibration number is reported in this release because no human labels were collected in this environment.
