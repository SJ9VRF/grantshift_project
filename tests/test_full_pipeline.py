from pathlib import Path
from grantshiftbench.loaders.jsonl import load_scenarios,select_split
from grantshift.policy.learned import LearnedPolicy
from grantshift.reward.pairwise import PairwiseRewardModel
from grantshift.types import Action

ROOT=Path(__file__).resolve().parents[1]

def test_v1_benchmark_size():
 s,l=load_scenarios(ROOT/"grantshiftbench/scenarios/v1.jsonl"); assert len(s)==600==len(l)

def test_split_sizes():
 s,l=load_scenarios(ROOT/"grantshiftbench/scenarios/v1.jsonl"); sp=ROOT/"grantshiftbench/scenarios/splits.json"
 import json
 splits=json.loads(sp.read_text())
 assert splits.get("version")=="2.0"
 assert len(select_split(s,l,sp,"train")[0])==len(splits["train"])
 assert len(select_split(s,l,sp,"dev")[0])==len(splits["dev"])
 assert len(select_split(s,l,sp,"test")[0])==len(splits["test"])
 assert len(splits["train"])+len(splits["dev"])+len(splits["test"])==600

def test_learned_policy_runs():
 s,l=load_scenarios(ROOT/"grantshiftbench/scenarios/v1.jsonl"); sp=ROOT/"grantshiftbench/scenarios/splits.json"
 tr,tl=select_split(s,l,sp,"train"); te,_=select_split(s,l,sp,"test")
 p=LearnedPolicy(calibrated=False).fit(tr,[x.preferred_action for x in tl]); assert p.decide(te[0]).action in Action
