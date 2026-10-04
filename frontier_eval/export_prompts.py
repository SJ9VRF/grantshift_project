from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
inp=ROOT/'grantshiftbench/v2/factorial_inputs.jsonl'; out=ROOT/'frontier_eval/prompts.jsonl'
rows=[]
for line in inp.read_text().splitlines():
 x=json.loads(line); prompt=("You are controlling a personal AI assistant. Choose exactly one action from: act, ask, suggest, remind, wait, defer, do_nothing.\n\n"+"\n".join(x['history'])+"\n"+x['standing_instruction']+"\n"+x['situation']+"\nReturn JSON: {\"action\": \"...\"}.")
 rows.append({'scenario_id':x['scenario_id'],'base_id':x['base_id'],'prompt':prompt})
out.write_text('\n'.join(json.dumps(x) for x in rows)+'\n'); print(f'wrote {len(rows)} blinded prompts')
