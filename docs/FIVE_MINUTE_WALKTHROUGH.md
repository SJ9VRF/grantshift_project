# GrantShift in Five Minutes

## 0:00-0:45 - The question
Personalization tells an agent what a user tends to want. It does not automatically tell the agent what it is authorized to do now. GrantShift asks whether an agent can preserve that distinction as authorization changes through time.

## 0:45-1:30 - The first falsification
A latest-label policy looks perfect on the easy transition suite. Bind grants to action scope/version and it starts executing stale permission. Bind grants to principal/request/resource/revision/nonce and it fails more sharply.

## 1:30-2:20 - The compositional failure
Authorization is a lifecycle, not a label. Expiry, revocation history, concurrent requests, replay, principal changes, and delegation ancestry compose. Flat provenance is still insufficient; a capability ledger is the explicit reference implementation for the synthetic instrument.

## 2:20-3:10 - We tried to break our own benchmark
The mutation suite intentionally deletes one invariant at a time. The first run exposed blind spots: some broken implementations still scored 100%. We added isolation families until every targeted mutant caused measurable failure. The release now fails if a targeted mutant escapes.

## 3:10-4:00 - Research engineering loop
The repository includes task generation, trajectory harnesses, state-based graders, repeated trials, incident mining, failure-to-training-pair export, claim-to-evidence gating, anonymous paper packaging, wheel/CLI packaging, and deterministic reproduction scripts.

## 4:00-5:00 - What is *not* claimed
The synthetic numbers do not establish frontier-model SOTA, human preference validity, or deployment safety. The next empirical step is to run the deduplicated frontier prompt pool on multiple GPT/Claude-class models, collect human authorization judgments, and port the protocol to an external interactive environment.

## Files to open
1. `paper/grantshift-paper-v1.4.0.pdf`
2. `project/trace_explorer.html`
3. `artifacts/capability_mutation_eval.json`
4. `docs/EVIDENCE_HIERARCHY.md`
5. `configs/claim_evidence_registry.json`
