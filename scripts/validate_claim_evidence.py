from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REG=ROOT/'configs/claim_evidence_registry.json'

def main():
    reg=json.loads(REG.read_text())
    missing=[]
    empty=[]
    for c in reg['claims']:
        for rel in c['evidence']:
            p=ROOT/rel
            if not p.exists(): missing.append({'claim':c['id'],'artifact':rel})
            elif p.stat().st_size == 0: empty.append({'claim':c['id'],'artifact':rel})
    report={
        'version':reg['version'],
        'claim_count':len(reg['claims']),
        'missing_evidence':missing,
        'empty_evidence':empty,
        'external_validation_claims':[c['id'] for c in reg['claims'] if c['external_validation_required']],
        'ready':not missing and not empty
    }
    (ROOT/'artifacts/claim_evidence_audit.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))
    raise SystemExit(0 if report['ready'] else 1)
if __name__=='__main__': main()
