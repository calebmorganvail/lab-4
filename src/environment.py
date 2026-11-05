"""Vacuum grid-world simulator for CS440 Lab 5."""

from __future__ import annotations

State = tuple[int, int]

GRID_ROWS = 4
GRID_COLS = 4
START_STATE: State = (0, 0)
DEFAULT_LIVING_REWARD = -0.04

_MOVES: dict[str, tuple[int, int]] = {
    "UP": (-1, 0),
    "DOWN": (1, 0),
    "LEFT": (0, -1),
    "RIGHT": (0, 1),
}


class VacuumGridEnv:
    """Deterministic 4x4 grid world for the vacuum robot.

    Layout (row, col), (0, 0) is the top-left::

        START  0   0   0
        0      X   0   0
        0      0   0   0
        0     -1   0  +10

    Rewards for the square the robot lands on:
        * goal (3, 3): +10 and the episode ends
        * penalty (3, 1): -1 (not terminal)
        * any other square, including bumping into a wall or edge: the living reward
    """

    def __init__(self, living_reward: float = DEFAULT_LIVING_REWARD) -> None:
        """Create the environment.

        Args:
            living_reward: reward for every move that does not land on the goal or penalty
                square. A small negative value pushes the robot to reach the goal quickly.
        """
        self._living_reward = living_reward
        self._walls: set[State] = {(1, 1)}
        self._special_rewards: dict[State, float] = {(3, 1): -1.0, (3, 3): 10.0}
        self._terminal_states: set[State] = {(3, 3)}
        self._state: State = START_STATE
        self._done = False

    @property
    def actions(self) -> list[str]:
        """The four available actions."""
        return list(_MOVES)

    def reset(self) -> State:
        """Put the robot back on the start square and return that state."""
        self._state = START_STATE
        self._done = False
        return self._state

    def step(self, action: str) -> tuple[State, float, bool]:
        """Move the robot one square.

        Args:
            action: one of "UP", "DOWN", "LEFT", "RIGHT".

        Returns:
            (next_state, reward, done)

        Raises:
            ValueError: if the action is not valid.
            RuntimeError: if called after the episode ended, before ``reset()``.
        """
        if self._done:
            raise RuntimeError("Episode is over; call reset() before step().")
        if action not in _MOVES:
            raise ValueError(f"Unknown action {action!r}; expected one of {self.actions}.")

        row_change, col_change = _MOVES[action]
        target = (self._state[0] + row_change, self._state[1] + col_change)
        if self._is_open(target):
            self._state = target

        reward = self._special_rewards.get(self._state, self._living_reward)
        self._done = self._state in self._terminal_states
        return self._state, reward, self._done

    def _is_open(self, cell: State) -> bool:
        """True if the cell is inside the grid and not a wall."""
        row, col = cell
        inside = 0 <= row < GRID_ROWS and 0 <= col < GRID_COLS
        return inside and cell not in self._walls
