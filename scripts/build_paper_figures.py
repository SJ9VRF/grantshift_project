from pathlib import Path
import json
import matplotlib.pyplot as plt
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'paper/figures'; OUT.mkdir(parents=True,exist_ok=True)
res=json.loads((ROOT/'artifacts/v2_factorial_results.json').read_text())
models=['C0_state_only','C1_state_plus_preference','C2_state_plus_authorization','C3_full','always_ask']
labels=['State','+ preference','+ authorization','Full','Always ask']
exact=[res[m]['exact'] for m in models]
unauth=[res[m]['unauthorized_act_rate'] for m in models]
burden=[res[m]['question_burden'] for m in models]
x=np.arange(len(models)); w=.25
fig,ax=plt.subplots(figsize=(8,4.2))
ax.bar(x-w,exact,w,label='Exact action match')
ax.bar(x,unauth,w,label='Unauthorized ACT')
ax.bar(x+w,burden,w,label='Question burden')
ax.set_xticks(x,labels,rotation=15,ha='right'); ax.set_ylim(0,1.05); ax.set_ylabel('Rate')
ax.legend(frameon=False,ncol=3,fontsize=8); ax.set_title('Preference, permission, and the cost of universal confirmation')
fig.tight_layout(); fig.savefig(OUT/'factorial_tradeoffs.pdf',bbox_inches='tight'); fig.savefig(OUT/'factorial_tradeoffs.png',dpi=180,bbox_inches='tight'); plt.close(fig)

surf=json.loads((ROOT/'artifacts/v2_surface_generalization.json').read_text())['C3_full_paraphrase']
canonical=res['C3_full']
metrics=['exact','acceptable','question_burden','synthetic_expected_utility']
clabels=['Exact','Acceptable','Question burden','Synthetic utility']
can=[canonical[m] for m in metrics]; par=[surf[m] for m in metrics]
x=np.arange(len(metrics)); w=.36
fig,ax=plt.subplots(figsize=(7.2,4))
ax.bar(x-w/2,can,w,label='Canonical surface')
ax.bar(x+w/2,par,w,label='Held-out paraphrase')
ax.axhline(0,linewidth=.8)
ax.set_xticks(x,clabels,rotation=12,ha='right'); ax.set_ylabel('Score / rate'); ax.legend(frameon=False); ax.set_title('Surface-form stress test exposes template sensitivity')
fig.tight_layout(); fig.savefig(OUT/'surface_generalization.pdf',bbox_inches='tight'); fig.savefig(OUT/'surface_generalization.png',dpi=180,bbox_inches='tight'); plt.close(fig)

lh=json.loads((ROOT/'artifacts/long_horizon_v2.json').read_text())
traj=lh['trajectory']; turns=[x['turn'] for x in traj]
def err(key): return [1 if x[key]!=x['preferred_action'] else 0 for x in traj]
frozen=np.cumsum(err('frozen_action'))/np.arange(1,len(traj)+1)
adapt=np.cumsum(err('adaptive_action'))/np.arange(1,len(traj)+1)
fig,ax=plt.subplots(figsize=(7.2,4))
ax.plot(turns,frozen,label='Frozen preference state')
ax.plot(turns,adapt,label='Adaptive preference state')
ax.axvline(lh['drift_turn'],linestyle='--',linewidth=1,label='Preference drift')
ax.set_ylim(-.02,1.02); ax.set_xlabel('Interaction turn'); ax.set_ylabel('Cumulative action error'); ax.legend(frameon=False); ax.set_title('Long-horizon synthetic preference drift')
fig.tight_layout(); fig.savefig(OUT/'long_horizon_drift.pdf',bbox_inches='tight'); fig.savefig(OUT/'long_horizon_drift.png',dpi=180,bbox_inches='tight'); plt.close(fig)
print('built figures:', ', '.join(p.name for p in OUT.glob('*.pdf')))


rob=json.loads((ROOT/'artifacts/v2_robustness_suite.json').read_text())
ctrl=rob['negative_controls']
names=['Canonical','Auth shuffled','Auth masked','Pref shuffled','Pref masked']
vals=[rob['canonical']['exact'],ctrl['authorization_shuffled']['exact'],ctrl['authorization_masked']['exact'],ctrl['preference_shuffled']['exact'],ctrl['preference_masked']['exact']]
una=[rob['canonical']['unauthorized_act_rate'],ctrl['authorization_shuffled']['unauthorized_act_rate'],ctrl['authorization_masked']['unauthorized_act_rate'],ctrl['preference_shuffled']['unauthorized_act_rate'],ctrl['preference_masked']['unauthorized_act_rate']]
x=np.arange(len(names)); w=.36
fig,ax=plt.subplots(figsize=(7.8,4.2))
ax.bar(x-w/2,vals,w,label='Exact action match')
ax.bar(x+w/2,una,w,label='Unauthorized ACT')
ax.set_xticks(x,names,rotation=16,ha='right'); ax.set_ylim(0,1.05); ax.set_ylabel('Rate'); ax.legend(frameon=False)
ax.set_title('Negative controls isolate the role of authorization evidence')
fig.tight_layout(); fig.savefig(OUT/'evidence_controls.pdf',bbox_inches='tight'); fig.savefig(OUT/'evidence_controls.png',dpi=180,bbox_inches='tight'); plt.close(fig)

aug=rob['surface_augmentation']
fig,ax=plt.subplots(figsize=(6.8,4.0))
labels2=['Canonical','Held-out paraphrase']
basevals=[rob['canonical']['exact'],rob['paraphrase']['exact']]
augvals=[aug['canonical']['exact'],aug['paraphrase']['exact']]
x=np.arange(2); w=.34
ax.bar(x-w/2,basevals,w,label='Canonical-only training')
ax.bar(x+w/2,augvals,w,label='Two-surface augmentation')
ax.set_xticks(x,labels2); ax.set_ylim(0,1.05); ax.set_ylabel('Exact action match'); ax.legend(frameon=False)
ax.set_title('Simple surface augmentation repairs the observed shortcut')
fig.tight_layout(); fig.savefig(OUT/'surface_augmentation.pdf',bbox_inches='tight'); fig.savefig(OUT/'surface_augmentation.png',dpi=180,bbox_inches='tight'); plt.close(fig)
