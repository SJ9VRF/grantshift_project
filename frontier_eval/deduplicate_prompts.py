from __future__ import annotations
import hashlib, json, re
from collections import OrderedDict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'frontier_eval/transition_prompts.jsonl'
OUT=ROOT/'frontier_eval/transition_prompts_unique.jsonl'
MAP=ROOT/'frontier_eval/prompt_equivalence_map.json'

def norm(s): return re.sub(r'\s+',' ',s.strip())

def main():
    groups=OrderedDict()
    for line in SRC.read_text().splitlines():
        if not line.strip(): continue
        r=json.loads(line); h=hashlib.sha256(norm(r['prompt']).encode()).hexdigest()
        if h not in groups: groups[h]={'representative':r,'scenario_ids':[]}
        groups[h]['scenario_ids'].append(r['scenario_id'])
    uniq=[]; eq={}
    for i,(h,g) in enumerate(groups.items()):
        r=dict(g['representative']); uid=f'gsu-{i:05d}'; r['unique_prompt_id']=uid; r['equivalent_scenario_count']=len(g['scenario_ids']); r['prompt_sha256']=h
        uniq.append(r); eq[uid]=g['scenario_ids']
    OUT.write_text('\n'.join(json.dumps(x) for x in uniq)+'\n')
    MAP.write_text(json.dumps({'n_full':sum(len(v) for v in eq.values()),'n_unique':len(uniq),'mapping':eq},indent=2)+'\n')
    print(json.dumps({'n_full':sum(len(v) for v in eq.values()),'n_unique':len(uniq),'reduction_fraction':1-len(uniq)/sum(len(v) for v in eq.values()),'output':str(OUT)},indent=2))
if __name__=='__main__':main()
