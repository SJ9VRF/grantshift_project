from pathlib import Path
import json, re
ROOT=Path(__file__).resolve().parents[1]
registry=json.loads((ROOT/'configs/claim_evidence_registry.json').read_text())
journal=(ROOT/'evidence/EXPERIMENT_JOURNAL.md').read_text()
entries={}
for m in re.finditer(r'^## (Exp-\d+) — (.+?)\n(.*?)(?=^## Exp-|\Z)', journal, re.M|re.S):
    eid,title,body=m.groups()
    ev=[]
    em=re.search(r'\*\*Evidence\.\*\* (.+)',body)
    if em: ev=re.findall(r'`([^`]+)`',em.group(1))
    entries[eid]={'id':eid,'title':title.strip(),'evidence':ev}
claim_nodes=[]
for c in registry['claims']:
    linked=[]
    ce=set(c['evidence'])
    for e in entries.values():
        if ce.intersection(e['evidence']): linked.append(e['id'])
    claim_nodes.append({**c,'experiments':linked})
out={'version':'1.7.0','claims':claim_nodes,'experiments':list(entries.values()),
     'integrity':{'claims_without_experiment_links':[c['id'] for c in claim_nodes if not c['experiments']],
                  'evidence_files_missing':sorted({f for c in claim_nodes for f in c['evidence'] if not (ROOT/f).exists()})}}
(ROOT/'evidence/EVIDENCE_GRAPH.json').write_text(json.dumps(out,indent=2)+'\n')
rows=[]
for c in claim_nodes:
    rows.append(f"<tr><td><code>{c['id']}</code></td><td>{c['claim']}</td><td>{', '.join(c['experiments']) or '—'}</td><td>"+'<br>'.join(f'<code>{x}</code>' for x in c['evidence'])+'</td></tr>')
html='''<!doctype html><meta charset="utf-8"><title>GrantShift Evidence Graph</title><style>body{font:15px system-ui;max-width:1180px;margin:40px auto;padding:0 24px;color:#171717}table{border-collapse:collapse;width:100%}th,td{border-bottom:1px solid #ddd;text-align:left;vertical-align:top;padding:10px}code{font-size:12px;background:#f3f3f3;padding:2px 4px}h1{font-size:34px}p{max-width:850px;line-height:1.55}</style><h1>GrantShift Evidence Graph</h1><p>Trace every public research claim to experiment-journal entries and raw artifacts. Empty experiment links are visible rather than silently inferred.</p><table><thead><tr><th>Claim</th><th>Statement</th><th>Experiments</th><th>Raw evidence</th></tr></thead><tbody>'''+''.join(rows)+'''</tbody></table>'''
(ROOT/'project/evidence_graph.html').write_text(html)
print(json.dumps(out['integrity'],indent=2))
