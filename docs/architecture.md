# Architecture

The repository separates **state estimation**, **decision policy**, **evaluation**, and **research artifacts** so each can change independently.

```text
User / environment state
        |
        v
AgentState + AutonomyProfile
        |
        +--> transparent risk estimate
        |
        +--> feature representation
                 |
                 v
        intervention policy
   heuristic / generic / personalized
                 |
                 v
 act | ask | suggest | remind | wait | defer | do nothing
                 |
                 v
   evaluation + calibration + failure analysis
```

## Design principles

1. **Silence is an action.** `DO_NOTHING`, `WAIT`, and `DEFER` are first-class decisions rather than absence of output.
2. **Personalization is explicit.** User autonomy preferences are separated from environmental state so contrastive tests can hold the state fixed and vary only the user.
3. **Risk is not confidence.** Intent confidence, execution confidence, stakes, and reversibility remain distinct features.
4. **Calibration is held out.** Temperature scaling fits only on the development set.
5. **Synthetic labels are bounded claims.** They support mechanism tests and regression testing, not claims about real human preferences.
6. **Every reported result is regenerable.** `make all` rebuilds data, trains/exports the policy, evaluates, tests, and audits the release.

## Deployable artifact

`training/export_policy.py` produces `artifacts/personalized_policy.joblib`, which contains the preprocessing pipeline, classifier, personalization configuration, and held-out calibration temperature. The `grantshift-agent` CLI loads this exact bundle for inference.
