# Testing Context (loaded on demand)

Loaded when the prompt mentions tests, pytest, bugs or debugging, or on a `test*` branch.
Read by `environment-builder` for its tests. `qlearning-agent` gets its own test list inline
because this file mentions grid coordinates.

- Framework: `pytest`, tests in `tests/`, files named `test_*.py`.
- Environment tests: wall blocks movement, edges block movement, -1 and +10 rewards,
  goal is terminal, `reset()` returns `(0, 0)`.
- Agent tests: Q-table starts at 0, one update matches the formula by hand,
  epsilon=0 always picks the argmax action, epsilon decays but never below its minimum.
- Integration test (`tests/test_integration.py`, written by the main session, not by
  `qlearning-agent`): with a fixed seed, after training the greedy policy from START reaches GOAL
  without stepping on (3, 1).
