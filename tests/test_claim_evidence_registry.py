import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def test_claim_registry_has_evidence():
    reg=json.loads((ROOT/'configs/claim_evidence_registry.json').read_text())
    assert len(reg['claims']) >= 6
    for c in reg['claims']:
        assert c['scope']
        assert c['evidence']
        for rel in c['evidence']:
            assert (ROOT/rel).exists(), rel

def test_unsupported_external_claims_are_explicitly_prohibited():
    reg=json.loads((ROOT/'configs/claim_evidence_registry.json').read_text())
    assert len(reg['prohibited_claims_without_external_evidence']) >= 4
