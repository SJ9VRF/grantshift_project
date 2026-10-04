from pathlib import Path
import json
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'artifacts/trajectory_eval.json').read_text())['summary']
out=ROOT/'paper/figures'; out.mkdir(parents=True,exist_ok=True)
order=['preference_only','always_ask','authorization_first_noisy8','authorization_first']
labels=['Preference only','Always ask','Auth-first + 8% noise','Authorization first']
vals=[data[k]['pass_rate']*100 for k in order]
cons=[data[k]['pass_pow_k']['5']*100 for k in order]
fig,ax=plt.subplots(figsize=(6.2,3.2))
x=range(len(order))
ax.bar([i-0.18 for i in x],vals,width=.36,label='pass@1')
ax.bar([i+0.18 for i in x],cons,width=.36,label='pass^5')
ax.set_ylim(0,105); ax.set_ylabel('Success (%)'); ax.set_xticks(list(x),labels,rotation=15,ha='right')
ax.legend(frameon=False); ax.set_title('Trajectory-level reliability separates average success from consistency')
fig.tight_layout(); fig.savefig(out/'trajectory_reliability.pdf'); plt.close(fig)

inc=json.loads((ROOT/'artifacts/incident_priorities.json').read_text())
fig,ax=plt.subplots(figsize=(6.2,3.2))
names=[x['failure_type'].replace('_',' ') for x in inc]
counts=[x['count'] for x in inc]
ax.barh(names[::-1],counts[::-1]); ax.set_xlabel('Mined failed trials'); ax.set_title('Failure mining produces a concrete post-training curriculum')
fig.tight_layout(); fig.savefig(out/'incident_mining.pdf'); plt.close(fig)

# Cross-environment state-tracking figure
cross_path=ROOT/'artifacts/cross_environment_eval.json'
if cross_path.exists():
    cross=json.loads(cross_path.read_text())['by_variant']
    variants=['standard','delayed_confirmation','revoked_after_confirmation','transient_tool_failure']
    labels_v=['Standard','Delayed confirm','Revoked','Tool failure']
    agents=['authorization_first','robust_authorization_first','robust_authorization_first_noisy8']
    agent_labels=['Static auth-first','State-tracking','State-tracking + 8% noise']
    fig,ax=plt.subplots(figsize=(6.4,3.3))
    xs=list(range(len(variants))); w=.24
    for j,(agent,label) in enumerate(zip(agents,agent_labels)):
        vals=[cross[agent][v]['pass_rate']*100 for v in variants]
        ax.bar([x+(j-1)*w for x in xs],vals,width=w,label=label)
    ax.set_ylim(0,105); ax.set_ylabel('Pass rate (%)'); ax.set_xticks(xs,labels_v,rotation=12,ha='right')
    ax.set_title('Environment shifts separate static rules from state tracking')
    ax.legend(frameon=False,fontsize=8)
    fig.tight_layout(); fig.savefig(out/'cross_environment_reliability.pdf'); plt.close(fig)
