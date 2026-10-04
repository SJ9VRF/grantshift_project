"""Utility and burden metrics for intervention policies.

The default weights are research knobs, not claims about human values. Human studies should
estimate or sensitivity-test them.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class UtilityWeights:
    task_success: float=1.0
    unauthorized_action: float=3.0
    question: float=0.25
    interruption: float=0.5
    missed_opportunity: float=0.75
    irreversible_error: float=4.0
