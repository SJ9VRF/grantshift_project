from pathlib import Path
import hashlib, json
ROOT=Path(__file__).resolve().parents[1]
files=[
    ROOT/'grantshiftbench/scenarios/v1.jsonl',
    ROOT/'grantshiftbench/scenarios/contrast_v1.jsonl',
    ROOT/'grantshiftbench/scenarios/frontier_v1.jsonl',
    ROOT/'grantshiftbench/scenarios/splits.json',
    ROOT/'grantshiftbench/generators/generate_v1.py',
    ROOT/'grantshiftbench/generators/generate_contrast.py',
    ROOT/'grantshiftbench/generators/generate_frontier.py',
    ROOT/'grantshiftbench/v2/factorial_inputs.jsonl',
    ROOT/'grantshiftbench/v2/factorial_gold.jsonl',
    ROOT/'grantshiftbench/v2/factorial_splits.json',
    ROOT/'grantshiftbench/v2/factorial_paraphrase_test_inputs.jsonl',
    ROOT/'grantshiftbench/v2/generate_factorial.py',
]
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
records=[]
for p in files:
    records.append({'path':str(p.relative_to(ROOT)),'sha256':sha(p),'bytes':p.stat().st_size})
out={
    'benchmark':'GrantShiftBench',
    'version':'1.4.0',
    'author':'Aura Yavary',
    'synthetic_oracle':True,
    'files':records,
    'counts':{'legacy_main':600,'legacy_contrastive_personalization':160,'legacy_authorization_frontier':240,'v2_factorial':6000,'v2_paraphrase_stress':900},
}
(ROOT/'grantshiftbench/PROVENANCE.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
