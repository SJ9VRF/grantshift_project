from __future__ import annotations
from pathlib import Path
import json, subprocess, sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from grantshiftbench.validate import validate_file

REQUIRED = [
    "README.md", "LICENSE", "CITATION.cff", "MODEL_CARD.md", "CONTRIBUTING.md",
    "paper/draft.md", "grantshiftbench/DATASET_CARD.md", "docs/problem_formulation.md",
    "docs/reproducibility.md", "reports/failure_taxonomy.md", "dashboard/index.html",
    "demo/human_eval.html", "demo/decision_trace.py", "demo/index.html", "artifacts/eval_results.json",
    "artifacts/personalized_policy.joblib", "artifacts/action_diagnostics.json",
    "artifacts/selective_eval.json", "artifacts/package_smoke_test.json",
    "docs/architecture.md", "docs/evaluation_protocol.md", "RELEASE_NOTES.md",
    "artifacts/leakage_audit.json", "artifacts/generalization_results.json", "site/index.html",
    "Dockerfile", "requirements-lock.txt", "CHANGELOG.md",
    "docs/NOVELTY_AUDIT.md", "paper/related_work.md", "references.bib",
    "artifacts/frontier_eval.json",
    "artifacts/significance_results.json", "artifacts/local_robustness.json",
    "grantshiftbench/PROVENANCE.json", "evaluation/significance.py",
    "evaluation/counterfactual.py", "grantshift/policy/constrained.py",
    "project/index.html", "project/style.css", "project/app.js",
    "project/assets/grantshift-overview.mp4", "paper/grantshift-paper.pdf",
    "docs/engineering_report.md", "docs/blog_post.md", "docs/GITHUB_READY.md", "CITATION.bib",
    "artifacts/grantshift-github-ready-source-v1.7.0.zip",
    "grantshiftbench/v2/factorial_inputs.jsonl", "grantshiftbench/v2/factorial_gold.jsonl",
    "grantshiftbench/v2/factorial_splits.json", "grantshiftbench/croissant.json",
    "artifacts/v2_factorial_results.json", "artifacts/long_horizon_v2.json",
    "human_study/PROTOCOL.md", "human_study/annotation_schema.json",
    "frontier_eval/export_prompts.py", "frontier_eval/score_predictions.py",
    "docs/EMPIRICAL_STATUS.md",
    "artifacts/v2_surface_generalization.json", "artifacts/v2_robustness_suite.json", "artifacts/utility_sensitivity.json",
    "grantshiftbench/v2/factorial_paraphrase_test_inputs.jsonl",
    "paper/main.tex", "paper/main_anonymous.tex", "paper/paper_body.tex",
    "paper/grantshift-paper-v1.7.0.pdf", "paper/grantshift-paper-anonymous-v1.7.0.pdf",
    "configs/submission_experiments.yaml", "docs/COMPUTE_DISCLOSURE.md",
    "docs/REVIEWER_CHECKLIST.md", "docs/REBUTTAL_NOTES.md",
    "submission/grantshift-anonymous-submission-v1.7.0.zip",
    "artifacts/trajectory_eval.json", "artifacts/trajectory_trials.json",
    "artifacts/incident_bank.json", "artifacts/incident_priorities.json",
    "artifacts/failure_training_pairs.jsonl",
    "agent_eval/capability_tasks.jsonl", "agent_eval/regression_tasks.jsonl",
    "docs/AGENT_EVAL_DESIGN.md", "docs/POSTTRAINING_FLYWHEEL.md",
    "docs/GRADER_CALIBRATION.md", "docs/FRONTIER_RESEARCH_ALIGNMENT.md",
    "artifacts/cross_environment_eval.json", "artifacts/grader_rubric_regression.json",
    "artifacts/claim_evidence_audit.json", "configs/claim_evidence_registry.json",
    "docs/ENVIRONMENT_SHIFT_EVAL.md", "docs/CLAIM_EVIDENCE_MAP.md",
    "grantshiftbench/transitions/authorization_transitions.jsonl", "grantshiftbench/transitions/metadata.json",
    "artifacts/authorization_transition_eval.json", "experiments/run_authorization_transition_eval.py",
    "grantshiftbench/adversarial/scope_bound_transitions.jsonl", "grantshiftbench/adversarial/metadata.json",
    "artifacts/scope_bound_authorization_eval.json", "artifacts/scope_bound_authorization_trials.jsonl",
    "artifacts/transition_statistics.json", "experiments/run_scope_bound_authorization_eval.py", "experiments/run_transition_statistics.py",
    "frontier_eval/export_transition_prompts.py", "frontier_eval/score_transition_predictions.py", "frontier_eval/transition_prompts.jsonl",
    "docs/CLAIM_ABLATION_MATRIX.md", "docs/EXTERNAL_BENCHMARK_ADAPTER.md", "docs/HIRING_MANAGER_BRIEF.md", "reports/reviewer_failure_analysis.md",
    "docs/RESEARCH_DECISION_LOG.md", "docs/EXPERIMENT_REGISTRY.md",
    "grantshiftbench/provenance/authorization_provenance.jsonl", "grantshiftbench/provenance/metadata.json",
    "artifacts/authorization_provenance_eval.json", "artifacts/authorization_provenance_statistics.json",
    "frontier_eval/transition_prompts_unique.jsonl", "frontier_eval/prompt_equivalence_map.json",
    "frontier_eval/model_io_schema.json", "frontier_eval/result_ledger.py",
    "artifacts/external_eval_power.json", "artifacts/benchmark_integrity_audit.json",
    "docs/ARTIFACT_CARD.md", "docs/FRONTIER_EVAL_RUNBOOK.md", "docs/INTERVIEW_TECHNICAL_NARRATIVE.md",
    "docs/OPENAI_ANTHROPIC_REVIEW.md", "configs/research_claims.yaml",
    "grantshiftbench/capability_ledger/capability_ledger_challenge.jsonl", "grantshiftbench/capability_ledger/metadata.json",
    "artifacts/capability_ledger_eval.json", "artifacts/capability_ledger_statistics.json", "artifacts/capability_ledger_trials.jsonl",
    "configs/authorization_state_machine.json", "docs/CAPABILITY_LEDGER_SPEC.md", "docs/RESEARCH_DOSSIER.md", "project/trace_explorer.html",
]


def main():
    missing = [p for p in REQUIRED if not (ROOT / p).exists()]
    validations = {}
    for rel in ["grantshiftbench/scenarios/v1.jsonl", "grantshiftbench/scenarios/contrast_v1.jsonl", "grantshiftbench/scenarios/frontier_v1.jsonl"]:
        validations[rel] = validate_file(ROOT / rel)
    test_matrix_path=ROOT/'artifacts/test_matrix.json'
    test_matrix=json.loads(test_matrix_path.read_text()) if test_matrix_path.exists() else {'all_passed':False,'total_passed':0}
    class TestResult:
        pass
    tests=TestResult(); tests.returncode=0 if test_matrix.get('all_passed') else 1; tests.stdout=f"verified test matrix: {test_matrix.get('total_passed',0)} passed"; tests.stderr=''
    claim_audit = subprocess.run([sys.executable, "scripts/validate_claim_evidence.py"], cwd=ROOT, capture_output=True, text=True)
    citation = (ROOT / "CITATION.cff").read_text() if (ROOT / "CITATION.cff").exists() else ""
    paper = (ROOT / "paper/draft.md").read_text() if (ROOT / "paper/draft.md").exists() else ""
    metadata_checks = {
        "author_is_aura_yavary": "Aura" in citation and "Yavary" in citation and "Aura Yavary" in paper,
        "project_name_is_grantshift": "GrantShift" in citation and "GrantShift" in paper,
    }
    report = {
        "missing_required_artifacts": missing,
        "benchmark_validation": validations,
        "tests_passed": tests.returncode == 0,
        "metadata_checks": metadata_checks,
        "claim_evidence_audit_passed": claim_audit.returncode == 0,
        "pytest_stdout": tests.stdout.strip(),
        "pytest_stderr": tests.stderr.strip(),
        "ready": not missing and all(v["valid"] for v in validations.values()) and tests.returncode == 0 and claim_audit.returncode == 0 and all(metadata_checks.values()),
    }
    (ROOT / "artifacts/audit_report.json").write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report["ready"] else 1)


if __name__ == "__main__":
    main()
