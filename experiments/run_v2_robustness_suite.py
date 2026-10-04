from pathlib import Path
import json, random, statistics, sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from experiments.run_v2_factorial import load_jsonl, text, metrics
from grantshiftbench.v2.generate_factorial import generate


def fit(xs, gs, condition='full'):
    return Pipeline([
        ('tfidf',TfidfVectorizer(ngram_range=(1,2),min_df=2,max_features=30000)),
        ('lr',LogisticRegression(max_iter=1000,class_weight='balanced'))
    ]).fit([text(x,condition) for x in xs],[g['preferred_action'] for g in gs])

def evaluate(model, xs, gs, condition='full'):
    return metrics(model.predict([text(x,condition) for x in xs]).tolist(), gs)

def main():
    inp=load_jsonl(ROOT/'grantshiftbench/v2/factorial_inputs.jsonl')
    gold=load_jsonl(ROOT/'grantshiftbench/v2/factorial_gold.jsonl'); gm={x['scenario_id']:x for x in gold}
    sp=json.loads((ROOT/'grantshiftbench/v2/factorial_splits.json').read_text())
    train_ids=set(sp['train']); test_ids=set(sp['test'])
    tr=[x for x in inp if x['base_id'] in train_ids]; tg=[gm[x['scenario_id']] for x in tr]
    te=[x for x in inp if x['base_id'] in test_ids]; eg=[gm[x['scenario_id']] for x in te]
    pte=load_jsonl(ROOT/'grantshiftbench/v2/factorial_paraphrase_test_inputs.jsonl')
    peg=load_jsonl(ROOT/'grantshiftbench/v2/factorial_paraphrase_test_gold.jsonl')

    base=fit(tr,tg)
    out={'metadata':{'name':'GrantShift v2 robustness suite','synthetic_labels':True,'test_n':len(te)}}
    out['canonical']=evaluate(base,te,eg)
    out['paraphrase']=evaluate(base,pte,peg)

    # Counterfactual evidence controls: corrupt one evidence channel while retaining gold.
    rng=random.Random(121)
    auth=[x['standing_instruction'] for x in te]; rng.shuffle(auth)
    auth_shuffle=[dict(x,standing_instruction=a) for x,a in zip(te,auth)]
    pref=[x['history'] for x in te]; rng.shuffle(pref)
    pref_shuffle=[dict(x,history=h) for x,h in zip(te,pref)]
    auth_mask=[dict(x,standing_instruction='') for x in te]
    pref_mask=[dict(x,history=[]) for x in te]
    out['negative_controls']={
        'authorization_shuffled':evaluate(base,auth_shuffle,eg),
        'authorization_masked':evaluate(base,auth_mask,eg),
        'preference_shuffled':evaluate(base,pref_shuffle,eg),
        'preference_masked':evaluate(base,pref_mask,eg),
    }

    # Surface augmentation uses a second deterministic rendering only for training base states.
    aug_rows,aug_gold=generate(seed=907,paraphrase=True,base_filter=train_ids)
    augmented=fit(tr+aug_rows,tg+aug_gold)
    out['surface_augmentation']={
        'canonical':evaluate(augmented,te,eg),
        'paraphrase':evaluate(augmented,pte,peg),
    }

    # Base-level subsampling robustness: five 90% train-base fits, fixed test.
    train_bases=sorted(train_ids); runs=[]
    for seed in [11,23,37,51,79]:
        rr=random.Random(seed); ids=train_bases[:]; rr.shuffle(ids); keep=set(ids[:int(.9*len(ids))])
        xs=[x for x in tr if x['base_id'] in keep]; gs=[gm[x['scenario_id']] for x in xs]
        m=fit(xs,gs); runs.append({'seed':seed,**evaluate(m,te,eg)})
    summary={}
    for k in ['exact','acceptable','unauthorized_act_rate','question_burden','synthetic_expected_utility']:
        vals=[r[k] for r in runs]
        summary[k]={'mean':statistics.mean(vals),'std':statistics.stdev(vals),'min':min(vals),'max':max(vals)}
    out['train_subsample_robustness']={'runs':runs,'summary':summary}

    # Leave-one-domain-out training evaluates semantic transfer across task families.
    domains=sorted({x['domain'] for x in inp}); loo={}
    for dom in domains:
        xs=[x for x in inp if x['domain']!=dom and x['base_id'] not in test_ids]
        gs=[gm[x['scenario_id']] for x in xs]
        tx=[x for x in te if x['domain']==dom]; gg=[gm[x['scenario_id']] for x in tx]
        m=fit(xs,gs)
        loo[dom]={'n':len(tx),**evaluate(m,tx,gg)}
    out['leave_one_domain_out']=loo

    (ROOT/'artifacts/v2_robustness_suite.json').write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()
