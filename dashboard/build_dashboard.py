from __future__ import annotations

from pathlib import Path
import html
import json

ROOT = Path(__file__).resolve().parents[1]


def load(name, default):
    p = ROOT / "artifacts" / name
    return json.loads(p.read_text()) if p.exists() else default


res = load("eval_results.json", {})
abl = load("ablation_results.json", {})
sel = load("selective_eval.json", {"points": []})
diag = load("action_diagnostics.json", {"errors": [], "per_action": {}})
contrast = load("contrast_results.json", {})
frontier = load("frontier_eval.json", {})
sig = load("significance_results.json", {})

models = ["heuristic", "generic_learned", "personalized_learned", "personalized_calibrated"]
rows = []
for k in models:
    v = res.get(k, {})
    ece = v.get("calibration", {}).get("ece", float("nan"))
    rows.append(
        f"<tr><td>{html.escape(k.replace('_',' '))}</td>"
        f"<td>{v.get('accuracy',0):.3f}</td><td>{v.get('acceptable_action_rate',0):.3f}</td>"
        f"<td>{v.get('false_proactivity_rate',0):.3f}</td><td>{v.get('missed_opportunity_rate',0):.3f}</td>"
        f"<td>{v.get('autonomy_violation_rate',0):.3f}</td><td>{ece:.3f}</td></tr>"
    )
rows = "".join(rows)

ablrows = "".join(
    f"<tr><td>{html.escape(k)}</td><td>{v.get('accuracy',0):.3f}</td><td>{v.get('missed_opportunity_rate',0):.3f}</td></tr>"
    for k, v in abl.items()
)

best = min(sel.get("points", []), key=lambda x: abs(x.get("threshold", 0) - 0.85), default={})
selective_rows = "".join(
    f"<tr><td>{p['threshold']:.2f}</td><td>{p['coverage']:.3f}</td><td>{p['exact_accuracy']:.3f}</td>"
    f"<td>{p['acceptable_rate']:.3f}</td><td>{p['severity_weighted_error']:.3f}</td></tr>"
    for p in sel.get("points", []) if p.get("exact_accuracy") is not None and p["threshold"] >= 0.5
)

def fmt(x):
    return "—" if x is None else f"{x:.3f}"

per_action_rows = "".join(
    f"<tr><td>{html.escape(action)}</td><td>{m['support']}</td><td>{m['predicted']}</td>"
    f"<td>{fmt(m['precision'])}</td>"
    f"<td>{fmt(m['recall'])}</td>"
    f"<td>{fmt(m['f1'])}</td></tr>"
    for action, m in diag.get("per_action", {}).items()
)

error_rows = "".join(
    f"<tr><td>{html.escape(e['scenario_id'])}</td><td>{html.escape(e['domain'])}</td>"
    f"<td>{html.escape(e['gold'])}</td><td>{html.escape(e['pred'])}</td><td>{e['severity']:.2f}</td>"
    f"<td>{html.escape(e['goal'])}</td></tr>" for e in diag.get("errors", [])[:8]
)


frontier_rows = "".join(
    f"<tr><td>{html.escape(k.replace('_',' '))}</td><td>{v.get('accuracy',0):.3f}</td><td>{v.get('acceptable_action_rate',0):.3f}</td><td>{v.get('false_proactivity_rate',0):.3f}</td><td>{v.get('mean_overreach_distance',0):.3f}</td><td>{v.get('all_four_acceptable_group_rate',0):.3f}</td></tr>"
    for k,v in frontier.items() if k != 'metadata'
)
main_sig = sig.get('main_generic_vs_personalized', {})
frontier_sig = sig.get('frontier_unconstrained_vs_authorization_first', {})

cal = res.get("personalized_calibrated", {})
contrast_generic = contrast.get("generic", {}).get("accuracy", 0)
contrast_personal = contrast.get("personalized", {}).get("accuracy", 0)

page = f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Proactivity Evaluation Dashboard</title><style>
:root{{--bg:#0c0e11;--panel:#14181d;--text:#f4f6f8;--muted:#9da7b2;--line:#283039;--accent:#d6ff4b}}*{{box-sizing:border-box}}body{{background:var(--bg);color:var(--text);font-family:Inter,ui-sans-serif,system-ui,sans-serif;max-width:1180px;margin:0 auto;padding:44px 22px 80px;line-height:1.5}}h1{{font-size:clamp(42px,7vw,78px);line-height:.96;letter-spacing:-.045em;margin:8px 0 16px}}h2{{font-size:18px}}p{{color:var(--muted)}}.eyebrow{{color:var(--accent);font-size:12px;font-weight:700;letter-spacing:.16em;text-transform:uppercase}}.cards{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:28px 0}}.metric,.card{{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:18px}}.metric b{{font-size:29px;display:block;letter-spacing:-.03em}}.metric span{{color:var(--muted);font-size:12px}}.card{{margin:16px 0;overflow:auto}}table{{border-collapse:collapse;width:100%;font-size:13px}}th,td{{padding:10px;border-bottom:1px solid var(--line);text-align:left;white-space:nowrap}}th{{color:var(--muted);font-weight:600}}code{{background:#20252b;padding:2px 6px;border-radius:6px}}.boundary{{border-left:3px solid var(--accent);padding-left:14px}}@media(max-width:800px){{.cards{{grid-template-columns:1fr 1fr}}}}@media(max-width:520px){{.cards{{grid-template-columns:1fr}}}}
</style></head><body><div class="eyebrow">Evaluation / GrantShiftBench v1</div><h1>GrantShift</h1><p>Controlled evaluation of personalized, calibrated intervention policies. All benchmark labels are synthetic-oracle labels.</p>
<div class="cards"><div class="metric"><b>{cal.get('accuracy',0):.1%}</b><span>personalized exact</span></div><div class="metric"><b>{cal.get('calibration',{}).get('ece',0):.3f}</b><span>held-out ECE</span></div><div class="metric"><b>{contrast_personal:.1%}</b><span>contrastive personalized</span></div><div class="metric"><b>{best.get('exact_accuracy',0):.1%}</b><span>accuracy @ 0.85 confidence</span></div></div>
<div class="card"><h2>Model comparison</h2><table><tr><th>Model</th><th>Exact</th><th>Acceptable</th><th>False proactive</th><th>Missed</th><th>Autonomy violation</th><th>ECE</th></tr>{rows}</table></div>
<div class="card"><h2>Contrastive personalization</h2><p>Matched opportunity states, different user autonomy profiles.</p><table><tr><th>Policy</th><th>Exact</th></tr><tr><td>Generic</td><td>{contrast_generic:.3f}</td></tr><tr><td>Personalized</td><td>{contrast_personal:.3f}</td></tr></table></div>
<div class="card"><h2>Authorization frontier</h2><p>60 matched base situations × four counterfactual authorization states. The fair generic+gate baseline is shown explicitly.</p><table><tr><th>Policy</th><th>Exact</th><th>Acceptable</th><th>False proactive</th><th>Mean overreach</th><th>All-4 acceptable groups</th></tr>{frontier_rows}</table></div>
<div class="card"><h2>Paired diagnostics</h2><p>Main generic→personalized: Δ exact {main_sig.get('paired_bootstrap',{}).get('delta_accuracy',0):.3f}, McNemar p={main_sig.get('mcnemar_exact',{}).get('p_value_two_sided',1):.3g}. Frontier unconstrained→authorization-first: Δ exact {frontier_sig.get('paired_bootstrap',{}).get('delta_accuracy',0):.3f}, McNemar p={frontier_sig.get('mcnemar_exact',{}).get('p_value_two_sided',1):.3g}. Synthetic benchmark only.</p></div>
<div class="card"><h2>Selective intervention</h2><p>Raising the confidence threshold sacrifices coverage in exchange for stronger intervention precision. Around 0.85, the current controlled test retains {best.get('coverage',0):.1%} coverage at {best.get('exact_accuracy',0):.1%} exact accuracy.</p><table><tr><th>Threshold</th><th>Coverage</th><th>Exact</th><th>Acceptable</th><th>Severity-weighted error</th></tr>{selective_rows}</table></div>
<div class="card"><h2>Per-action diagnostics</h2><table><tr><th>Action</th><th>Gold support</th><th>Predicted</th><th>Precision</th><th>Recall</th><th>F1</th></tr>{per_action_rows}</table></div>
<div class="card"><h2>Highest-severity test errors</h2><table><tr><th>ID</th><th>Domain</th><th>Gold</th><th>Pred</th><th>Severity</th><th>Goal</th></tr>{error_rows}</table></div>
<div class="card"><h2>Ablations</h2><table><tr><th>Configuration</th><th>Accuracy</th><th>Missed opportunity</th></tr>{ablrows}</table></div>
<div class="card boundary"><h2>Interpretation boundary</h2><p>These results demonstrate the mechanics of personalization, calibration, abstention, drift, and regression testing under a transparent synthetic oracle. They do not establish real-user preference validity.</p></div>
<div class="card"><h2>Decision space</h2><p><code>ACT</code> · <code>ASK</code> · <code>SUGGEST</code> · <code>REMIND</code> · <code>WAIT</code> · <code>DEFER</code> · <code>DO_NOTHING</code></p></div></body></html>"""
(ROOT / "dashboard/index.html").write_text(page)
print(ROOT / "dashboard/index.html")
