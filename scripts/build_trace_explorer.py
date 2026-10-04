from __future__ import annotations
import html, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TR=ROOT/'artifacts/capability_ledger_trials.jsonl'; OUT=ROOT/'project/trace_explorer.html'
rows=[json.loads(x) for x in TR.read_text().splitlines() if x.strip()]
# Keep representative failures from simple baselines plus matched ledger traces.
keys=[]
for r in rows:
    if not r['exact'] and r['policy']!='capability_ledger':
        k=(r['trajectory_id'],r['family']);
        if k not in keys: keys.append(k)
    if len(keys)>=30: break
selected=[r for r in rows if (r['trajectory_id'],r['family']) in keys]
payload=json.dumps(selected).replace('</','<\\/')
page=f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>GrantShift Trace Explorer</title><style>
body{{font:15px/1.45 system-ui,-apple-system,sans-serif;background:#0b0d10;color:#e8edf2;margin:0}}main{{max-width:1100px;margin:auto;padding:32px}}
h1{{font-size:34px;margin-bottom:4px}}.sub{{color:#9aa7b5;margin-bottom:24px}}select{{background:#161b22;color:#fff;border:1px solid #30363d;padding:9px 12px;border-radius:8px;margin-right:8px}}
.card{{background:#11161c;border:1px solid #27303a;border-radius:12px;padding:16px;margin:14px 0}}.bad{{border-left:4px solid #ff7b72}}.ok{{border-left:4px solid #3fb950}}
code{{color:#a5d6ff}}.meta{{color:#8b949e;font-size:13px}}.act{{font-weight:700}} table{{width:100%;border-collapse:collapse}}td,th{{padding:8px;border-bottom:1px solid #27303a;text-align:left;vertical-align:top}}
</style></head><body><main><h1>GrantShift Trace Explorer</h1><div class="sub">Representative capability-ledger failures. Synthetic mechanism traces; not frontier-model outputs.</div>
<div><select id="fam"></select><select id="traj"></select></div><div id="view"></div></main>
<script>const rows={payload}; const fam=document.getElementById('fam'),traj=document.getElementById('traj'),view=document.getElementById('view');
const families=[...new Set(rows.map(x=>x.family))]; fam.innerHTML='<option value="all">All families</option>'+families.map(x=>`<option>${{x}}</option>`).join('');
function sync(){{let rs=rows.filter(x=>fam.value==='all'||x.family===fam.value); let ids=[...new Set(rs.map(x=>x.trajectory_id))]; traj.innerHTML=ids.map(x=>`<option>${{x}}</option>`).join(''); render();}}
function render(){{let rs=rows.filter(x=>x.trajectory_id===traj.value); let policies=[...new Set(rs.map(x=>x.policy))]; view.innerHTML=policies.map(p=>{{let xs=rs.filter(x=>x.policy===p).sort((a,b)=>a.step-b.step);return `<div class="card ${{xs.some(x=>!x.exact)?'bad':'ok'}}"><h3>${{p}}</h3><div class="meta">${{xs[0]?.family||''}} · ${{xs[0]?.domain||''}}</div><table><tr><th>Step</th><th>Event</th><th>Gold</th><th>Pred</th><th>Validity</th></tr>`+xs.map(x=>`<tr><td>${{x.step}}</td><td>${{x.event.event}}</td><td class="act">${{x.gold_action}}</td><td class="act">${{x.predicted_action}}</td><td>${{x.invalid_capability_execution?'INVALID EXECUTION':'ok'}}</td></tr>`).join('')+'</table></div>'}}).join('');}}
fam.onchange=sync; traj.onchange=render; sync();</script></body></html>'''
OUT.write_text(page); print(OUT)
