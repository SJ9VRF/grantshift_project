.PHONY: all v2 utility trajectory crossenv rubric claims scope paper submission benchmark validate leakage train eval diagnostics selective generalization frontier significance robustness ablations contrast reward drift dashboard report test audit clean

v2:
	PYTHONPATH=. python grantshiftbench/v2/generate_factorial.py
	PYTHONPATH=. python experiments/run_v2_factorial.py
	PYTHONPATH=. python experiments/run_v2_surface_generalization.py
	PYTHONPATH=. python experiments/run_v2_robustness_suite.py
	PYTHONPATH=. python experiments/run_long_horizon_v2.py
	PYTHONPATH=. python frontier_eval/export_prompts.py
	PYTHONPATH=. python human_study/power_analysis.py > artifacts/power_analysis.json

transitions:
	PYTHONPATH=. python grantshiftbench/transitions/generate.py
	PYTHONPATH=. python experiments/run_authorization_transition_eval.py

scope: transitions
	PYTHONPATH=. python grantshiftbench/adversarial/generate.py
	PYTHONPATH=. python experiments/run_scope_bound_authorization_eval.py
	PYTHONPATH=. python experiments/run_transition_statistics.py
	PYTHONPATH=. python frontier_eval/export_transition_prompts.py

ledger:
	PYTHONPATH=. python -m grantshiftbench.capability_ledger.generate
	PYTHONPATH=. python experiments/run_capability_ledger_eval.py
	PYTHONPATH=. python experiments/run_capability_ledger_statistics.py
	PYTHONPATH=. python experiments/run_capability_mutation_eval.py
	PYTHONPATH=. python scripts/build_trace_explorer.py

utility:
	PYTHONPATH=. python experiments/run_utility_sensitivity.py

trajectory:
	PYTHONPATH=. python experiments/run_agent_trajectory_eval.py
	PYTHONPATH=. python -m agent_eval.export_tasks


crossenv:
	PYTHONPATH=. python experiments/run_cross_environment_eval.py


rubric:
	PYTHONPATH=. python evaluation/run_grader_rubric_regression.py


claims: crossenv rubric
	PYTHONPATH=. python scripts/validate_claim_evidence.py


paper: scope ledger v2 utility trajectory crossenv rubric claims
	PYTHONPATH=. python scripts/build_paper_figures.py
	PYTHONPATH=. python scripts/build_agent_eval_figures.py
	cd paper && pdflatex -interaction=nonstopmode main.tex >/dev/null && (/usr/bin/bibtex.original main >/dev/null || true) && pdflatex -interaction=nonstopmode main.tex >/dev/null && pdflatex -interaction=nonstopmode main.tex >/dev/null
	cd paper && pdflatex -interaction=nonstopmode main_anonymous.tex >/dev/null && (/usr/bin/bibtex.original main_anonymous >/dev/null || true) && pdflatex -interaction=nonstopmode main_anonymous.tex >/dev/null && pdflatex -interaction=nonstopmode main_anonymous.tex >/dev/null
	cp paper/main.pdf paper/grantshift-paper.pdf
	cp paper/main.pdf paper/grantshift-paper-v1.4.0.pdf
	cp paper/main_anonymous.pdf paper/grantshift-paper-anonymous-v1.4.0.pdf

submission: paper
	PYTHONPATH=. python scripts/build_anonymous_submission.py

benchmark:
	PYTHONPATH=. python grantshiftbench/generators/generate_v1.py
	PYTHONPATH=. python grantshiftbench/generators/generate_contrast.py
	PYTHONPATH=. python grantshiftbench/generators/generate_frontier.py
	PYTHONPATH=. python grantshiftbench/build_splits.py

validate: benchmark
	PYTHONPATH=. python scripts/build_provenance.py
	PYTHONPATH=. python grantshiftbench/validate.py grantshiftbench/scenarios/v1.jsonl
	PYTHONPATH=. python grantshiftbench/validate.py grantshiftbench/scenarios/contrast_v1.jsonl
	PYTHONPATH=. python grantshiftbench/validate.py grantshiftbench/scenarios/frontier_v1.jsonl

leakage: validate
	PYTHONPATH=. python scripts/leakage_audit.py

train: leakage
	PYTHONPATH=. python training/export_policy.py

eval: train
	PYTHONPATH=. python experiments/run_full_eval.py

diagnostics: eval
	PYTHONPATH=. python experiments/run_action_diagnostics.py

selective: eval
	PYTHONPATH=. python experiments/run_selective_eval.py

generalization: eval
	PYTHONPATH=. python experiments/run_generalization_eval.py

frontier: eval
	PYTHONPATH=. python experiments/run_frontier_eval.py

significance: frontier
	PYTHONPATH=. python experiments/run_significance.py

robustness: eval
	PYTHONPATH=. python experiments/run_local_robustness.py

ablations:
	PYTHONPATH=. python experiments/run_ablations.py

contrast:
	PYTHONPATH=. python experiments/run_contrast_eval.py

reward:
	PYTHONPATH=. python experiments/run_preference_reward.py

drift:
	PYTHONPATH=. python experiments/run_drift_simulation.py

dashboard:
	PYTHONPATH=. python dashboard/build_dashboard.py

report:
	PYTHONPATH=. python scripts/build_report.py

test:
	PYTHONPATH=. pytest -q

audit:
	PYTHONPATH=. python scripts/audit_repo.py

all: scope ledger v2 trajectory crossenv rubric claims benchmark validate leakage train eval diagnostics selective generalization frontier significance robustness ablations contrast reward drift dashboard report test audit

clean:
	rm -rf .pytest_cache **/__pycache__ artifacts/*.json
