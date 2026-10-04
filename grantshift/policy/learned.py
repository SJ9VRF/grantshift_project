from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable
import math
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from grantshift.features.vectorize import state_to_record
from grantshift.types import AgentState, Action, Decision
from grantshift.risk.estimator import estimate_risk


@dataclass
class LearnedPolicy:
    """Interpretable classical baseline with optional held-out temperature calibration.

    Calibration intentionally uses a distinct development split rather than reusing
    the training data. This keeps the engineering baseline honest and avoids the
    appearance of evaluating calibration on data used to fit the classifier.
    """

    include_personalization: bool = True
    calibrated: bool = False
    feature_groups: set[str] | None = None
    model: object | None = None
    temperature: float = 1.0

    def _records(self, states):
        return [state_to_record(s, self.include_personalization, self.feature_groups) for s in states]

    def fit(self, states: Iterable[AgentState], actions: Iterable[Action]):
        states = list(states)
        actions = list(actions)
        X = pd.DataFrame(self._records(states))
        y = [a.value for a in actions]
        if X.empty:
            raise ValueError("empty training set")

        numeric = [
            c for c in X.columns
            if pd.api.types.is_numeric_dtype(X[c]) and c != "goal"
        ]
        categorical = [c for c in X.columns if c not in numeric and c != "goal"]

        transformers = []
        if numeric:
            transformers.append(("num", Pipeline([
                ("imp", SimpleImputer()),
                ("scale", StandardScaler()),
            ]), numeric))
        if categorical:
            transformers.append(("cat", OneHotEncoder(handle_unknown="ignore"), categorical))
        if "goal" in X.columns:
            transformers.append(("goal", TfidfVectorizer(ngram_range=(1, 2), min_df=1), "goal"))

        pre = ColumnTransformer(transformers)
        clf = LogisticRegression(max_iter=3000, class_weight="balanced", C=2.0)
        self.model = Pipeline([("pre", pre), ("clf", clf)])
        self.model.fit(X, y)
        self.temperature = 1.0
        return self

    def calibrate(self, states: Iterable[AgentState], actions: Iterable[Action]):
        """Fit one scalar temperature on a held-out calibration set.

        A deterministic log-spaced grid avoids adding another optimization dependency.
        The selected temperature minimizes multiclass negative log likelihood.
        """
        if self.model is None:
            raise RuntimeError("fit before calibrate")
        states = list(states)
        actions = list(actions)
        if not states:
            raise ValueError("empty calibration set")

        X = pd.DataFrame(self._records(states))
        raw = np.clip(self.model.predict_proba(X), 1e-12, 1.0)
        classes = list(self.model.classes_)
        targets = np.array([classes.index(a.value) for a in actions], dtype=int)

        def transform(probs, temp):
            powered = np.power(probs, 1.0 / temp)
            return powered / powered.sum(axis=1, keepdims=True)

        best_t, best_nll = 1.0, math.inf
        for t in np.logspace(-1.0, 1.0, 161):
            p = np.clip(transform(raw, float(t)), 1e-12, 1.0)
            nll = float(-np.log(p[np.arange(len(p)), targets]).mean())
            if nll < best_nll:
                best_t, best_nll = float(t), nll
        self.temperature = best_t
        self.calibrated = True
        return self

    def _apply_temperature(self, probs: np.ndarray) -> np.ndarray:
        if not self.calibrated or abs(self.temperature - 1.0) < 1e-12:
            return probs
        powered = np.power(np.clip(probs, 1e-12, 1.0), 1.0 / self.temperature)
        return powered / powered.sum()

    def predict_proba(self, state: AgentState) -> dict[Action, float]:
        if self.model is None:
            raise RuntimeError("policy not fit")
        X = pd.DataFrame(self._records([state]))
        probs = self._apply_temperature(self.model.predict_proba(X)[0])
        classes = self.model.classes_
        return {Action(c): float(p) for c, p in zip(classes, probs)}

    def decide(self, state: AgentState) -> Decision:
        probs = self.predict_proba(state)
        action = max(probs, key=probs.get)
        risk = estimate_risk(state)
        confidence = probs[action]
        top = sorted(probs.items(), key=lambda kv: kv[1], reverse=True)[:3]
        reasons = [f"learned policy: {a.value}={p:.2f}" for a, p in top]
        if self.calibrated:
            reasons.append(f"held-out temperature={self.temperature:.3f}")
        return Decision(
            action=action,
            utility=state.expected_benefit - risk,
            risk=risk,
            reasons=reasons,
            confidence=confidence,
        )
