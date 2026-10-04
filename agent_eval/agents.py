from __future__ import annotations
import random
from grantshift.types import Action
from .schema import AgentTask

class PreferenceOnlyAgent:
    name = "preference_only"
    def reset(self, task: AgentTask, seed: int): self.task, self.rng = task, random.Random(seed)
    def act(self, observation: str, env_state: dict) -> Action:
        return self.task.state.user_profile.preference_for(self.task.state.domain)

class AuthorizationFirstAgent:
    name = "authorization_first"
    def reset(self, task: AgentTask, seed: int): self.task, self.rng = task, random.Random(seed)
    def act(self, observation: str, env_state: dict) -> Action:
        auth = env_state["authorization"]
        pref = self.task.state.user_profile.preference_for(self.task.state.domain)
        if auth == "prohibited": return Action.DO_NOTHING
        if auth == "ask_required": return Action.ASK
        if auth == "advisory":
            return Action.REMIND if pref == Action.REMIND else Action.SUGGEST
        if not self.task.recoverable:
            return Action.DEFER if env_state.get("asked_user") else Action.ASK
        return Action.ACT if pref in {Action.ACT, Action.ASK, Action.SUGGEST} else pref

class RobustAuthorizationAgent:
    """State-tracking policy for shifted environments.

    Unlike the simple authorization-first baseline, this policy waits for pending
    confirmation, respects revocation observed in the latest state, and retries a
    recoverable action after a transient tool failure that happened before mutation.
    """
    name = "robust_authorization_first"
    def reset(self, task: AgentTask, seed: int):
        self.task, self.rng = task, random.Random(seed)
        self.last_observation = ""
    def act(self, observation: str, env_state: dict) -> Action:
        self.last_observation = observation
        auth = env_state["authorization"]
        pref = self.task.state.user_profile.preference_for(self.task.state.domain)
        if auth == "prohibited": return Action.DO_NOTHING
        if env_state.get("pending_confirmation"):
            return Action.WAIT
        if auth == "ask_required": return Action.ASK
        if auth == "advisory":
            return Action.REMIND if pref == Action.REMIND else Action.SUGGEST
        if not self.task.recoverable:
            return Action.DEFER if env_state.get("asked_user") else Action.ASK
        # ACT is safe when preauthorized and recoverable; repeated ACT is allowed
        # after a transient pre-mutation tool failure.
        return Action.ACT

class AlwaysAskAgent:
    name = "always_ask"
    def reset(self, task: AgentTask, seed: int): self.task = task
    def act(self, observation: str, env_state: dict) -> Action:
        if env_state["authorization"] == "preauthorized" and env_state["asked_user"]:
            return Action.ACT
        return Action.ASK

class NoisyAgent:
    """Adds seeded execution noise so repeated trials measure reliability."""
    def __init__(self, base, error_rate: float = 0.08):
        self.base, self.error_rate = base, error_rate
        self.name = f"{base.name}_noisy{int(error_rate*100)}"
    def reset(self, task: AgentTask, seed: int):
        self.base.reset(task, seed)
        self.rng = random.Random(seed + 991)
    def act(self, observation: str, env_state: dict) -> Action:
        a = self.base.act(observation, env_state)
        if self.rng.random() >= self.error_rate: return a
        alternatives = [x for x in Action if x != a]
        return self.rng.choice(alternatives)
