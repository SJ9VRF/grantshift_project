from __future__ import annotations
import argparse,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('predictions'); ap.add_argument('--map',default=str(ROOT/'frontier_eval/prompt_equivalence_map.json')); ap.add_argument('--out',default=str(ROOT/'artifacts/frontier_predictions_expanded.jsonl')); args=ap.parse_args()
    mapping=json.loads(Path(args.map).read_text())['mapping']; preds=[json.loads(x) for x in Path(args.predictions).read_text().splitlines() if x.strip()]
    out=[]
    for r in preds:
        uid=r.get('unique_prompt_id')
        if uid not in mapping: raise ValueError(f'unknown unique_prompt_id: {uid}')
        for sid in mapping[uid]:
            x=dict(r); x['scenario_id']=sid; x['expanded_from_unique_prompt_id']=uid; out.append(x)
    Path(args.out).write_text('\n'.join(json.dumps(x) for x in out)+'\n'); print(json.dumps({'n_input':len(preds),'n_expanded':len(out),'output':args.out},indent=2))
if __name__=='__main__':main()
