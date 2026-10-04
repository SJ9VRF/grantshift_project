# Environment-shift evaluation

The base decision benchmark assumes the authorization state is stable. Real agents cannot make that assumption. GrantShift v1.4 adds controlled state transitions that test whether a policy follows the **latest** environment state rather than repeating a rule derived from the initial request.

## Variants

- **Delayed confirmation:** after `ASK`, the response remains pending. The correct behavior is to wait, then act only after the confirmation resolves.
- **Permission revocation:** a confirmation is followed by an immediate revocation before execution. The correct behavior is to stop.
- **Transient tool failure:** an authorized, recoverable action fails before external mutation. A safe retry is allowed.
- **Standard controls:** matched non-shifted tasks remain in the suite.

## Executed release

- 90 tasks
- 3 policies
- 5 trials per task
- 1,350 total trajectories

| Policy | Pass rate | Authorization pass | State tracking | pass^5 |
|---|---:|---:|---:|---:|
| Authorization first | 80.0% | 100.0% | 66.7% | 32.8% |
| Robust authorization first | 100.0% | 100.0% | 100.0% | 100.0% |
| Robust + 8% action noise | 90.7% | 98.4% | 92.2% | 61.3% |

The static policy's failure is concentrated: it scores 0% on delayed-confirmation tasks because it asks repeatedly instead of representing a pending response. This is a state-tracking failure, not an authorization-rule failure.

The suite is synthetic and deterministic. It is designed as an executable regression mechanism, not as evidence about frontier-model deployment reliability.
