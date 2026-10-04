from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
R = json.loads((ROOT / "artifacts/eval_results.json").read_text())
C = json.loads((ROOT / "artifacts/contrast_results.json").read_text())
D = json.loads((ROOT / "artifacts/drift_results.json").read_text())
P = json.loads((ROOT / "artifacts/reward_model_results.json").read_text())
S = json.loads((ROOT / "artifacts/selective_eval.json").read_text())
F = json.loads((ROOT / "artifacts/frontier_eval.json").read_text())
G = json.loads((ROOT / "artifacts/generalization_results.json").read_text())
SIG = json.loads((ROOT / "artifacts/significance_results.json").read_text())
ROB = json.loads((ROOT / "artifacts/local_robustness.json").read_text())

models = ["heuristic", "generic_learned", "personalized_learned", "personalized_calibrated"]
lines = [
    "# Experiment Summary",
    "",
    "All numbers below are from a deterministic **synthetic-oracle benchmark**. They validate the research machinery and controlled causal contrasts; they are not evidence of human preference validity.",
    "",
    "## Main held-out test split",
    "",
    "| Model | Exact | 95% bootstrap CI | Acceptable | False proactive | Missed opportunity | Autonomy violation | Top-label ECE |",
    "|---|---:|---:|---:|---:|---:|---:|---:|",
]
for m in models:
    x = R[m]
    ci = x["accuracy_ci95"]
    ece = x.get("calibration", {}).get("ece", float("nan"))
    lines.append(
        f"| {m.replace('_',' ')} | {x['accuracy']:.3f} | [{ci['low']:.3f}, {ci['high']:.3f}] | "
        f"{x['acceptable_action_rate']:.3f} | {x['false_proactivity_rate']:.3f} | {x['missed_opportunity_rate']:.3f} | "
        f"{x['autonomy_violation_rate']:.3f} | {ece:.3f} |"
    )

cal = R["personalized_calibrated"]
lines += [
    "",
    "The calibrated policy fits a single scalar temperature on the **held-out development split** and then evaluates once on test. This avoids calibrating on the evaluation set.",
    f"Selected temperature: **{cal['temperature']:.3f}**.",
    "",
    "## Contrastive personalization set",
    "",
    "The same underlying opportunity states are paired with different user autonomy profiles. This isolates whether user-conditioned information changes the intervention decision.",
    "",
    "| Model | Exact | False proactive |",
    "|---|---:|---:|",
    f"| Generic | {C['generic']['accuracy']:.3f} | {C['generic']['false_proactivity_rate']:.3f} |",
    f"| Personalized | {C['personalized']['accuracy']:.3f} | {C['personalized']['false_proactivity_rate']:.3f} |",
    "",
    "## Matched intervention-frontier set",
    "",
    "This 240-case set holds 60 base situations approximately fixed while counterfactually changing authorization. It exposes a failure hidden by IID personalization accuracy.",
    "",
    "| Policy | Exact | Acceptable | False proactive | Mean overreach |",
    "|---|---:|---:|---:|---:|",
    f"| Generic | {F['generic']['accuracy']:.3f} | {F['generic']['acceptable_action_rate']:.3f} | {F['generic']['false_proactivity_rate']:.3f} | {F['generic']['mean_overreach_distance']:.3f} |",
    f"| Generic + authorization gate | {F['generic_authorization_first']['accuracy']:.3f} | {F['generic_authorization_first']['acceptable_action_rate']:.3f} | {F['generic_authorization_first']['false_proactivity_rate']:.3f} | {F['generic_authorization_first']['mean_overreach_distance']:.3f} |",
    f"| Personalized, unconstrained | {F['personalized_unconstrained']['accuracy']:.3f} | {F['personalized_unconstrained']['acceptable_action_rate']:.3f} | {F['personalized_unconstrained']['false_proactivity_rate']:.3f} | {F['personalized_unconstrained']['mean_overreach_distance']:.3f} |",
    f"| GrantShift authorization-first | {F['grantshift_authorization_first']['accuracy']:.3f} | {F['grantshift_authorization_first']['acceptable_action_rate']:.3f} | {F['grantshift_authorization_first']['false_proactivity_rate']:.3f} | {F['grantshift_authorization_first']['mean_overreach_distance']:.3f} |",
    f"| GrantShift constrained ranker | {F['grantshift_constrained_ranker']['accuracy']:.3f} | {F['grantshift_constrained_ranker']['acceptable_action_rate']:.3f} | {F['grantshift_constrained_ranker']['false_proactivity_rate']:.3f} | {F['grantshift_constrained_ranker']['mean_overreach_distance']:.3f} |",
    "",
    "The authorization-first rule is explicit: **authorization > recoverability > personalization**.",
    "",
    "## OOD stress tests",
    "",
    f"Held-out domains: personalized exact **{G['ood_domain']['personalized']['accuracy']:.3f}**, acceptable **{G['ood_domain']['personalized']['acceptable_action_rate']:.3f}**.",
    f"Held-out triggers: personalized exact **{G['ood_trigger']['personalized']['accuracy']:.3f}**, acceptable **{G['ood_trigger']['personalized']['acceptable_action_rate']:.3f}**, false-proactivity **{G['ood_trigger']['personalized']['false_proactivity_rate']:.3f}**. The trigger failure is intentionally retained.",
    "",
    "## Selective intervention / calibrated restraint",
    "",
    "Instead of forcing an intervention decision at every state, we can require a minimum calibrated confidence. This explicitly tests whether uncertainty can be converted into restraint.",
    "",
    "| Confidence threshold | Coverage | Exact | Acceptable | Severity-weighted error |",
    "|---:|---:|---:|---:|---:|",
    *[f"| {x['threshold']:.2f} | {x['coverage']:.3f} | {x['exact_accuracy']:.3f} | {x['acceptable_rate']:.3f} | {x['severity_weighted_error']:.3f} |" for x in S["points"] if x["threshold"] in (0.70, 0.80, 0.85, 0.90)],
    "",

    "## Paired statistical diagnostics",
    "",
    f"Main generic→personalized exact delta: **{SIG['main_generic_vs_personalized']['paired_bootstrap']['delta_accuracy']:.3f}**, paired-bootstrap 95% CI **[{SIG['main_generic_vs_personalized']['paired_bootstrap']['ci95'][0]:.3f}, {SIG['main_generic_vs_personalized']['paired_bootstrap']['ci95'][1]:.3f}]**, exact McNemar p=**{SIG['main_generic_vs_personalized']['mcnemar_exact']['p_value_two_sided']:.3g}**.",
    f"Frontier unconstrained→authorization-first exact delta: **{SIG['frontier_unconstrained_vs_authorization_first']['paired_bootstrap']['delta_accuracy']:.3f}**, 95% CI **[{SIG['frontier_unconstrained_vs_authorization_first']['paired_bootstrap']['ci95'][0]:.3f}, {SIG['frontier_unconstrained_vs_authorization_first']['paired_bootstrap']['ci95'][1]:.3f}]**, exact McNemar p=**{SIG['frontier_unconstrained_vs_authorization_first']['mcnemar_exact']['p_value_two_sided']:.3g}**.",
    "These tests describe this deterministic synthetic benchmark; they do not establish population-level human significance.",
    "",
    "## Local numeric perturbation stability",
    "",
    f"Action stability under ±0.01 normalized numeric jitter: **{ROB['0.01']['action_stability']:.3f}**; under ±0.05 jitter: **{ROB['0.05']['action_stability']:.3f}**. This is a sensitivity diagnostic, not a correctness claim.",
    "## Pairwise preference/reward baseline",
    "",
    f"Exact accuracy: **{P['accuracy']:.3f}**  ",
    f"Acceptable-action rate: **{P['acceptable_action_rate']:.3f}**  ",
    f"False-proactivity rate: **{P['false_proactivity_rate']:.3f}**",
    "",
    "## Preference drift",
    "",
    "| Policy state | Pre-drift | Post-drift |",
    "|---|---:|---:|",
    f"| Frozen | {D['frozen_pre']:.3f} | {D['frozen_post']:.3f} |",
    f"| Adaptive | {D['adaptive_pre']:.3f} | {D['adaptive_post']:.3f} |",
    "",
    "## Interpretation boundary",
    "",
    "The benchmark intentionally exposes controlled behavior differences, but it does not establish that the oracle's intervention preferences match real users. Publication-grade claims require blinded human annotation, inter-annotator agreement, natural-language scenario validation, and evaluation against external agent/model backends.",
]
(ROOT / "reports/experiment_summary.md").write_text("\n".join(lines) + "\n")
print("wrote reports/experiment_summary.md")
