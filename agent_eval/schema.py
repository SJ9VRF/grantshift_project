from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any
from grantshift.types import Action, AgentState

@dataclass
class AgentTask:
    task_id: str
    state: AgentState
    authorization: str
    recoverable: bool
    user_confirms_if_asked: bool
    max_turns: int = 4
    tags: list[str] = field(default_factory=list)

@dataclass
class TrajectoryStep:
    turn: int
    action: Action
    observation: str
    environment_before: dict[str, Any]
    environment_after: dict[str, Any]
    latency_ms: float

@dataclass
class GraderResult:
    grader: str
    score: float
    passed: bool
    details: dict[str, Any] = field(default_factory=dict)

@dataclass
class TrialRecord:
    task_id: str
    trial_id: int
    agent_name: str
    seed: int
    trajectory: list[TrajectoryStep]
    outcome: dict[str, Any]
    graders: list[GraderResult]
    passed: bool

    def to_dict(self):
        d = asdict(self)
        for step in d["trajectory"]:
            step["action"] = step["action"].value if isinstance(step["action"], Action) else step["action"]
        return d
