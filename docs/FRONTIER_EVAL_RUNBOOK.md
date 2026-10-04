# Frontier Evaluation Runbook

This is the execution plan for turning GrantShift from a synthetic mechanism paper into a frontier-model empirical study.

## Primary evaluation unit

Use **trajectory**, not prompt, as the statistical unit. Prompts belonging to one trajectory are correlated because they describe sequential authorization states.

## Model panel

Use at least three frontier-capable agent models and at least three stochastic runs per model when the provider supports stochasticity. Freeze model versions and record provider, model identifier, date, decoding parameters, tool configuration, and system prompt.

## Prompt set

- Full weighted records: `frontier_eval/transition_prompts.jsonl` (8,892 records)
- Cost-efficient exact-unique pool: `frontier_eval/transition_prompts_unique.jsonl` (1,602 prompts)
- Equivalence expansion: `frontier_eval/prompt_equivalence_map.json`

Run the unique pool once per model/run, then expand outputs using `frontier_eval/expand_unique_predictions.py` before scoring. This preserves benchmark weighting without paying for identical prompts repeatedly.

## Output contract

Each prediction must follow `frontier_eval/model_io_schema.json` and include:

- `scenario_id` or `unique_prompt_id` before expansion;
- one action from the fixed action vocabulary;
- model, provider, run ID;
- decoding metadata where available;
- latency and token accounting where available.

Use `frontier_eval/result_ledger.py` to create a run ledger and detect duplicate scenario outputs.

## Primary metrics

1. exact transition compliance;
2. stale-authority / stale-scope / invalid-provenance execution;
3. premature autonomous execution;
4. repeated confirmation burden;
5. authorization-update latency;
6. family-stratified failure rate;
7. run-to-run variance and pass^k for repeated trajectories.

## Statistics

- trajectory-cluster bootstrap 95% confidence intervals;
- paired exact/McNemar comparisons on the same scenarios;
- family-level error decomposition;
- hierarchical or cluster-aware modeling once repeated model runs exist;
- report raw counts, not only percentages.

`artifacts/external_eval_power.json` contains conservative sample-size planning examples. Re-estimate power after a pilot because paired predictions are correlated.

## Contamination and leakage language

Do not claim that proprietary frontier models were not trained on GrantShift or related material: that is not externally verifiable. The local integrity audit only checks IDs, exact prompt duplication, and direct benchmark-label leakage.

## Stop conditions

Do not publish a model ranking if:

- model versions are not pinned;
- >1% of required predictions are missing;
- prompt parsing failures are silently coerced;
- duplicate outputs inflate sample size;
- confidence intervals or run-to-run variance are omitted;
- the primary metric is changed after seeing model results without disclosure.
