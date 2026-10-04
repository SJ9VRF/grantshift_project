# GrantShift Artifact Card

**Project:** GrantShift  
**Author:** Aura Yavary  
**Primary research question:** Can a personalized agent track authorization as a time-varying, scope- and provenance-bound state rather than treating user preference or the latest permission label as transferable authority?

## What is executable

- controlled authorization-transition generator and evaluator;
- scope/version-bound adversarial generator and evaluator;
- authorization-provenance challenge binding grants to principal, request, resource, revision, and nonce;
- trajectory sandbox with state mutation and outcome-based graders;
- repeated-trial reliability metrics;
- failure mining and training-pair export;
- provider-neutral frontier-eval prompt/scoring format;
- unique-prompt external pool with expansion back to the full weighted benchmark;
- human-study protocol and power-analysis tooling;
- claim-to-evidence, benchmark-integrity, anonymization, and release audits.

## Evidence tiers

1. **Synthetic mechanism evidence:** completed locally. Shows that the benchmark distinguishes intentionally different policies and exposes stale-grant shortcuts.
2. **Research-infrastructure evidence:** completed locally. Shows that runs, traces, incidents, and result ledgers are reproducible.
3. **Frontier-model evidence:** not yet collected. The release contains 1,602 unique external prompts representing 8,892 weighted benchmark records.
4. **Human-validity evidence:** not yet collected. Protocol and annotation schema are included.
5. **Production safety evidence:** not claimed.

## Headline synthetic falsification tests

- latest authorization label: 100% on the easy transition suite, 88.9% on scope-bound authorization, and 66.7% on provenance-bound authorization;
- latest-label invalid-provenance execution: 33.3% on the provenance challenge;
- provenance-aware state machine: 100% exact / 0% invalid-provenance execution in the deterministic instrument.

These values validate the **instrument**, not a frontier model.

## External-eval budget discipline

The internal benchmark intentionally contains lexical replicates. Running every duplicate through a paid frontier API would waste budget and overweight duplicated surfaces. `frontier_eval/deduplicate_prompts.py` reduces 8,892 records to **1,602 exact-unique prompts** while retaining an equivalence map so outputs can be expanded back to the weighted benchmark.

## Reproduction

```bash
python grantshiftbench/transitions/generate.py
python grantshiftbench/adversarial/generate.py
python grantshiftbench/provenance/generate.py
python experiments/run_authorization_transition_eval.py
python experiments/run_scope_bound_authorization_eval.py
python experiments/run_authorization_provenance_eval.py
python experiments/run_provenance_statistics.py
python frontier_eval/export_transition_prompts.py
python frontier_eval/deduplicate_prompts.py
python scripts/audit_benchmark_integrity.py
pytest -q
```

## Non-claims

GrantShift does not currently claim frontier-model SOTA, human preference validity, deployment safety, or a demonstrated post-training improvement on a production model.
