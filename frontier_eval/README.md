# Frontier-model evaluation harness

This directory is intentionally provider-neutral. It exports blinded prompts and scores externally generated JSONL predictions. No frontier-model results are claimed until actual provider outputs are supplied.

Run:

```bash
python frontier_eval/export_prompts.py
# run prompts through the model/provider of choice, preserving scenario_id
python frontier_eval/score_predictions.py predictions.jsonl
```
