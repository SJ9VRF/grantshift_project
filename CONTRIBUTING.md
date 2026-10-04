# Contributing

Contributions should preserve the central distinction between **capability** and **intervention judgment**. New benchmark cases should specify the user profile, opportunity state, preferred action, acceptable alternatives, explicitly bad actions, and wrong-action severity.

## Development

```bash
pip install -e . pytest
make all
python scripts/audit_repo.py
```

## Benchmark changes

1. Keep scenario IDs unique and deterministic.
2. Keep every numeric state variable in `[0, 1]`.
3. Ensure the preferred action is in `acceptable_actions`.
4. Never place the same action in both `acceptable_actions` and `bad_actions`.
5. Add a regression test for every fixed failure mode.
6. Do not report synthetic-oracle results as human preference validity.

## Pull requests

Explain the hypothesis, expected behavior change, affected metrics, and any regression risk. If an intervention policy becomes more aggressive, report false-proactivity and autonomy-violation changes explicitly.
