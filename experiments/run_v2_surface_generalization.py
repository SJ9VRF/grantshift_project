from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from experiments.run_v2_factorial import load_jsonl, text, metrics

def main():
    inp=load_jsonl(ROOT/'grantshiftbench/v2/factorial_inputs.jsonl')
    gold=load_jsonl(ROOT/'grantshiftbench/v2/factorial_gold.jsonl'); gm={x['scenario_id']:x for x in gold}
    sp=json.loads((ROOT/'grantshiftbench/v2/factorial_splits.json').read_text()); train=set(sp['train'])
    tr=[x for x in inp if x['base_id'] in train]; tg=[gm[x['scenario_id']] for x in tr]
    y=[g['preferred_action'] for g in tg]
    model=Pipeline([('tfidf',TfidfVectorizer(ngram_range=(1,2),min_df=2,max_features=30000)),('lr',LogisticRegression(max_iter=1000,class_weight='balanced'))]).fit([text(x,'full') for x in tr],y)
    pin=load_jsonl(ROOT/'grantshiftbench/v2/factorial_paraphrase_test_inputs.jsonl')
    pgold=load_jsonl(ROOT/'grantshiftbench/v2/factorial_paraphrase_test_gold.jsonl')
    pred=model.predict([text(x,'full') for x in pin]).tolist()
    out={'metadata':{'evaluation':'held-out surface-form paraphrase stress test','n':len(pin),'training_surface':'canonical','test_surface':'unseen deterministic paraphrases','synthetic_labels':True},'C3_full_paraphrase':metrics(pred,pgold)}
    (ROOT/'artifacts/v2_surface_generalization.json').write_text(json.dumps(out,indent=2)); print(json.dumps(out,indent=2))
if __name__=='__main__': main()
