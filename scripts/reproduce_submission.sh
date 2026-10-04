#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
export PYTHONPATH=.
python grantshiftbench/v2/generate_factorial.py
python experiments/run_v2_factorial.py
python experiments/run_v2_surface_generalization.py
python experiments/run_v2_robustness_suite.py
python experiments/run_utility_sensitivity.py
python experiments/run_long_horizon_v2.py
python grantshiftbench/transitions/generate.py
python experiments/run_authorization_transition_eval.py
python grantshiftbench/adversarial/generate.py
python experiments/run_scope_bound_authorization_eval.py
python experiments/run_transition_statistics.py
python grantshiftbench/provenance/generate.py
python experiments/run_authorization_provenance_eval.py
python experiments/run_provenance_statistics.py
python frontier_eval/export_transition_prompts.py
python frontier_eval/deduplicate_prompts.py
python experiments/run_external_power_analysis.py
python scripts/audit_benchmark_integrity.py
python experiments/run_agent_trajectory_eval.py
python -m agent_eval.export_tasks
python human_study/power_analysis.py > artifacts/power_analysis.json
python frontier_eval/export_prompts.py
python scripts/build_paper_figures.py
python scripts/build_agent_eval_figures.py
python -m pytest -q tests/test_v2_factorial.py tests/test_agent_eval_harness.py tests/test_failure_flywheel.py
cd paper
pdflatex -interaction=nonstopmode main.tex >/tmp/grantshift_main_1.log
BIBTEX="$(command -v bibtex || true)"
if [[ -z "$BIBTEX" || ! -x "$BIBTEX" ]]; then BIBTEX=/usr/bin/bibtex.original; fi
"$BIBTEX" main >/tmp/grantshift_bib_main.log
pdflatex -interaction=nonstopmode main.tex >/tmp/grantshift_main_2.log
pdflatex -interaction=nonstopmode main.tex >/tmp/grantshift_main_3.log
pdflatex -interaction=nonstopmode main_anonymous.tex >/tmp/grantshift_anon_1.log
"$BIBTEX" main_anonymous >/tmp/grantshift_bib_anon.log
pdflatex -interaction=nonstopmode main_anonymous.tex >/tmp/grantshift_anon_2.log
pdflatex -interaction=nonstopmode main_anonymous.tex >/tmp/grantshift_anon_3.log
cp main.pdf grantshift-paper-v1.4.0.pdf
cp main_anonymous.pdf grantshift-paper-anonymous-v1.4.0.pdf
printf 'Submission-facing artifacts reproduced successfully.\n'
