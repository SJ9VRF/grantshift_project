
const TRAJ = [{"authorization": "advisory", "goal": "Advance a routines goal triggered by price_change", "profile": "autonomy_first", "recoverable": true, "personalized_base": "remind", "grantshift_action": "remind", "preferred": "remind", "acceptable": ["remind", "suggest"], "confidence": 0.992, "risk": 0.146, "reasons": ["learned policy: suggest=0.01", "learned policy: do_nothing=0.00"]}, {"authorization": "ask_required", "goal": "Advance a routines goal triggered by price_change", "profile": "autonomy_first", "recoverable": true, "personalized_base": "remind", "grantshift_action": "ask", "preferred": "ask", "acceptable": ["ask", "suggest"], "confidence": 0.984, "risk": 0.146, "reasons": ["learned policy: ask=0.00", "authorization-first: confirmation required -> ask"]}, {"authorization": "preauthorized", "goal": "Advance a routines goal triggered by price_change", "profile": "autonomy_first", "recoverable": true, "personalized_base": "remind", "grantshift_action": "remind", "preferred": "remind", "acceptable": ["remind", "suggest"], "confidence": 0.986, "risk": 0.146, "reasons": ["learned policy: do_nothing=0.01", "learned policy: suggest=0.01"]}, {"authorization": "prohibited", "goal": "Advance a routines goal triggered by price_change", "profile": "autonomy_first", "recoverable": true, "personalized_base": "remind", "grantshift_action": "do_nothing", "preferred": "do_nothing", "acceptable": ["do_nothing", "wait", "defer"], "confidence": 0.965, "risk": 0.146, "reasons": ["learned policy: suggest=0.00", "authorization-first: explicit prohibition -> do_nothing"]}];
function renderTrajectory(i){
 const d=TRAJ[i];
 document.querySelectorAll('.seg button').forEach((b,j)=>b.classList.toggle('active',j===i));
 document.getElementById('auth').textContent=d.authorization.replace('_',' ');
 document.getElementById('baseAction').textContent=d.personalized_base;
 document.getElementById('decision').textContent=d.grantshift_action;
 document.getElementById('gold').textContent=d.preferred;
 document.getElementById('confidence').textContent=d.confidence.toFixed(3);
 document.getElementById('risk').textContent=d.risk.toFixed(3);
 document.getElementById('reason').textContent=d.reasons.join(' · ');
 document.getElementById('acceptable').textContent=d.acceptable.join(' / ');
}
document.addEventListener('DOMContentLoaded',()=>renderTrajectory(0));
