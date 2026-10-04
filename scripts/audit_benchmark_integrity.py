from __future__ import annotations
import hashlib, json, re
from collections import Counter, defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'artifacts/benchmark_integrity_audit.json'
SOURCES={
 'transitions':ROOT/'grantshiftbench/transitions/authorization_transitions.jsonl',
 'scope_bound':ROOT/'grantshiftbench/adversarial/scope_bound_transitions.jsonl',
 'provenance':ROOT/'grantshiftbench/provenance/authorization_provenance.jsonl',
}

def norm(s): return re.sub(r'\s+',' ',re.sub(r'[^a-z0-9 ]',' ',s.lower())).strip()

def main():
    ids=[]; row_hashes=[]; family_counts=Counter(); findings=[]
    for suite,path in SOURCES.items():
        rows=[json.loads(x) for x in path.read_text().splitlines() if x.strip()]
        for r in rows:
            rid=f"{suite}:{r['trajectory_id']}"; ids.append(rid); family_counts[f"{suite}:{r.get('transition_type',r.get('family','unknown'))}"]+=1
            # Exact semantic-row hash excludes random noise and trajectory id.
            payload={k:v for k,v in r.items() if k not in {'trajectory_id','seed_noise'}}
            row_hashes.append((suite,hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest()))
    dup_ids=len(ids)-len(set(ids))
    hashes=Counter(h for _,h in row_hashes); duplicate_semantic_rows=sum(c-1 for c in hashes.values() if c>1)
    # Prompt integrity: labels must not be present as dedicated machine fields in exported prompt records.
    prompt_path=ROOT/'frontier_eval/transition_prompts.jsonl'
    prompt_rows=[json.loads(x) for x in prompt_path.read_text().splitlines() if x.strip()]
    duplicate_prompt_ids=len(prompt_rows)-len({r['scenario_id'] for r in prompt_rows})
    exact_prompt_duplicates=len(prompt_rows)-len({hashlib.sha256(norm(r['prompt']).encode()).hexdigest() for r in prompt_rows})
    unique_path=ROOT/'frontier_eval/transition_prompts_unique.jsonl'
    unique_rows=[json.loads(x) for x in unique_path.read_text().splitlines() if x.strip()]
    unique_duplicate_prompts=len(unique_rows)-len({hashlib.sha256(norm(r['prompt']).encode()).hexdigest() for r in unique_rows})
    prohibited_field_tokens=['gold_action','predicted_action','exact_rate','invalid_provenance_execution']
    leaked={tok:sum(tok in r['prompt'] for r in prompt_rows) for tok in prohibited_field_tokens}
    ready=dup_ids==0 and duplicate_prompt_ids==0 and unique_duplicate_prompts==0 and all(v==0 for v in leaked.values())
    out={
      'ready':ready,'trajectory_ids':len(ids),'duplicate_trajectory_ids':dup_ids,
      'semantic_duplicate_rows':duplicate_semantic_rows,
      'prompt_records_full':len(prompt_rows),'duplicate_prompt_ids':duplicate_prompt_ids,'exact_prompt_duplicates_full_pool':exact_prompt_duplicates,
      'prompt_records_unique':len(unique_rows),'exact_prompt_duplicates_unique_pool':unique_duplicate_prompts,
      'prohibited_field_token_hits':leaked,'family_counts':dict(sorted(family_counts.items())),
      'scope_note':'This audit checks release integrity, exact duplication, IDs, and direct label leakage. It cannot establish absence of contamination in proprietary model pretraining data.'
    }
    OUT.write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))
    if not ready: raise SystemExit(2)
if __name__=='__main__':main()
