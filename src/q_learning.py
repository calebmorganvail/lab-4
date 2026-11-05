"""Tabular Q-learning agent with epsilon-greedy exploration.

The agent knows nothing about the environment beyond the list of action names.
States are any hashable value (in this project, ``(row, col)`` tuples).
"""

from __future__ import annotations

import random
from typing import Hashable

State = Hashable

DEFAULT_LEARNING_RATE: float = 0.1
DEFAULT_DISCOUNT_FACTOR: float = 0.9
DEFAULT_EPSILON: float = 1.0
DEFAULT_EPSILON_MIN: float = 0.05
DEFAULT_EPSILON_DECAY: float = 0.995


class QLearningAgent:
    """Tabular Q-learning agent.

    The Q-table is a dict ``{state: {action: value}}``; unseen states are
    added lazily with every action set to 0.0.
    """

    def __init__(
        self,
        actions: list[str],
        learning_rate: float = DEFAULT_LEARNING_RATE,
        discount_factor: float = DEFAULT_DISCOUNT_FACTOR,
        epsilon: float = DEFAULT_EPSILON,
        epsilon_min: float = DEFAULT_EPSILON_MIN,
        epsilon_decay: float = DEFAULT_EPSILON_DECAY,
        seed: int | None = None,
    ) -> None:
        """Create an agent.

        Raises:
            ValueError: if actions is empty or any hyperparameter is out of range.
        """
        if not actions:
            raise ValueError("actions must be non-empty")
        if not 0.0 < learning_rate <= 1.0:
            raise ValueError("learning_rate must be in (0, 1]")
        if not 0.0 <= discount_factor <= 1.0:
            raise ValueError("discount_factor must be in [0, 1]")
        if not 0.0 <= epsilon <= 1.0:
            raise ValueError("epsilon must be in [0, 1]")
        if not 0.0 <= epsilon_min <= 1.0:
            raise ValueError("epsilon_min must be in [0, 1]")
        if epsilon_min > epsilon:
            raise ValueError("epsilon_min must not exceed epsilon")
        if not 0.0 < epsilon_decay <= 1.0:
            raise ValueError("epsilon_decay must be in (0, 1]")

        self.actions: list[str] = list(actions)
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.q_table: dict[State, dict[str, float]] = {}
        self._rng = random.Random(seed)

    def get_q_values(self, state: State) -> dict[str, float]:
        """Return the action-value row for a state, creating it (zeros) if new."""
        if state not in self.q_table:
            self.q_table[state] = {action: 0.0 for action in self.actions}
        return self.q_table[state]

    def best_action(self, state: State) -> str:
        """Return the argmax action for a state, breaking ties randomly."""
        q_values = self.get_q_values(state)
        best_value = max(q_values.values())
        best_actions = [a for a in self.actions if q_values[a] == best_value]
        return self._rng.choice(best_actions)

    def choose_action(self, state: State) -> str:
        """Pick an action epsilon-greedily."""
        if self._rng.random() < self.epsilon:
            return self._rng.choice(self.actions)
        return self.best_action(state)

    def update(
        self,
        state: State,
        action: str,
        reward: float,
        next_state: State,
        done: bool,
    ) -> float:
        """Apply one Q-learning update and return the new Q(state, action).

        When done is True the future term is 0 and next_state is not added
        to the Q-table.

        Raises:
            ValueError: if action is not a known action.
        """
        if action not in self.actions:
            raise ValueError(f"unknown action: {action!r}")
        q_values = self.get_q_values(state)
        future_value = 0.0 if done else max(self.get_q_values(next_state).values())
        target = reward + self.discount_factor * future_value
        q_values[action] += self.learning_rate * (target - q_values[action])
        return q_values[action]

    def decay_epsilon(self) -> float:
        """Decay epsilon (floored at epsilon_min) and return the new value."""
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
        return self.epsilon

    def greedy_policy(self) -> dict[State, str]:
        """Return the best action per known state; ties go to the first action."""
        policy: dict[State, str] = {}
        for state, q_values in self.q_table.items():
            policy[state] = max(self.actions, key=lambda a: q_values[a])
        return policy
