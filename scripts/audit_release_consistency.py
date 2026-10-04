from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
ledger=json.loads((ROOT/'artifacts/capability_ledger_eval.json').read_text())
mut=json.loads((ROOT/'artifacts/capability_mutation_eval.json').read_text())
expected={
 'n_trajectories':ledger['n_trajectories'],
 'n_steps':ledger['policies']['capability_ledger']['steps'],
 'latest_exact_pct':round(100*ledger['policies']['latest_authorization_label']['exact_rate'],1),
 'latest_invalid_pct':round(100*ledger['policies']['latest_authorization_label']['invalid_capability_execution_rate'],1),
 'flat_exact_pct':round(100*ledger['policies']['flat_provenance']['exact_rate'],1),
 'ledger_exact_pct':round(100*ledger['policies']['capability_ledger']['exact_rate'],1),
 'ledger_invalid_pct':round(100*ledger['policies']['capability_ledger']['invalid_capability_execution_rate'],1),
 'mutation_gate':bool(mut['release_gate']['all_targeted_mutants_detected'])
}
checks=[]
for rel in ['project/index.html','evidence/REAL_EVAL_TABLES.md','README.md']:
    p=ROOT/rel; txt=p.read_text(); normalized=txt.replace(',', '')
    must=[str(expected['n_trajectories']),str(expected['n_steps'])]
    if rel!='README.md': must += [f"{expected['latest_invalid_pct']:.1f}",f"{expected['ledger_invalid_pct']:.1f}"]
    missing=[x for x in must if x not in normalized]
    checks.append({'file':rel,'missing_expected_literals':missing,'pass':not missing})
# Prevent stale public package links.
home=(ROOT/'project/index.html').read_text()
stale=sorted(set(re.findall(r'v1\.[0-6]\.0',home)))
checks.append({'file':'project/index.html','stale_release_refs':stale,'pass':not stale})
report={'expected':expected,'checks':checks,'ready':all(c['pass'] for c in checks)}
(ROOT/'artifacts/release_consistency_audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
raise SystemExit(0 if report['ready'] else 1)
