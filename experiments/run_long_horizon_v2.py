from pathlib import Path
import json, random
ROOT=Path(__file__).resolve().parents[1]

def simulate(turns=100,drift_turn=40,seed=11):
    rng=random.Random(seed); true='confirm'; inferred='confirm'; stale='confirm'; rows=[]
    corrections=0; stale_overreach=0; adaptive_overreach=0
    for t in range(turns):
      if t==drift_turn: true='minimal'
      # an explicit correction is observed with 65% probability when a mismatched intervention occurs
      stale_action='ask' if stale=='confirm' else ('suggest' if stale=='autonomous' else 'do_nothing')
      adaptive_action='ask' if inferred=='confirm' else ('suggest' if inferred=='autonomous' else 'do_nothing')
      wanted='ask' if true=='confirm' else ('suggest' if true=='autonomous' else 'do_nothing')
      if stale_action!=wanted and stale_action!='do_nothing': stale_overreach+=1
      if adaptive_action!=wanted and adaptive_action!='do_nothing': adaptive_overreach+=1
      if adaptive_action!=wanted and rng.random()<.65:
        inferred=true; corrections+=1
      rows.append({'turn':t,'true_preference':true,'frozen_action':stale_action,'adaptive_action':adaptive_action,'preferred_action':wanted})
    return {'turns':turns,'drift_turn':drift_turn,'corrections':corrections,'frozen_overreach_after_drift':sum(r['turn']>=drift_turn and r['frozen_action']!=r['preferred_action'] for r in rows)/(turns-drift_turn),'adaptive_overreach_after_drift':sum(r['turn']>=drift_turn and r['adaptive_action']!=r['preferred_action'] for r in rows)/(turns-drift_turn),'adaptation_latency_turns':next((r['turn']-drift_turn for r in rows if r['turn']>=drift_turn and r['adaptive_action']==r['preferred_action']),None),'trajectory':rows}
if __name__=='__main__':
    out=simulate(); (ROOT/'artifacts/long_horizon_v2.json').write_text(json.dumps(out,indent=2)); print(json.dumps({k:v for k,v in out.items() if k!='trajectory'},indent=2))
