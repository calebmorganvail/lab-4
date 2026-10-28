# Project Memory – Vacuum Robot Q-Learning (CS440 Lab 4, Team 17)

<!-- Strategy 1 (Write): project-level persistent memory. Loaded every session and shared
     with the whole team through git. Keep it short and always-relevant; longer, task-specific
     context lives in .claude/context/ and is loaded on demand. -->

## Goal
Build a vacuum robot agent that learns to reach the goal square of a 4x4 grid world using
**Q-learning**. The agent is NOT given the transition model T or the reward function R.

## Core environment (always needed)
@.claude/context/environment.md

## Non-negotiable rules
- The agent must never read T, R or the grid layout directly. It only interacts through
  `env.reset()` and `env.step(action) -> (next_state, reward, done)`.
- Keep the environment (`src/environment.py`) and the learner (`src/q_learning.py`) in separate files.
- Do not hardcode the optimal path or policy anywhere.
- Use a fixed random seed for any experiment we report so results are reproducible.

## Architecture (planned)
```
src/environment.py   # VacuumGridEnv: grid simulator (knows T and R; hidden from the agent)
src/q_learning.py    # QLearningAgent: Q-table, epsilon-greedy, update rule
src/main.py          # training loop, prints learned Q-table and policy
tests/               # pytest unit tests
```

## Code standards
- Python 3.10+, standard library + numpy only (no RL libraries such as gym/stable-baselines).
- Type hints on all functions; docstrings on public classes and methods.
- Descriptive names (`learning_rate`, not `lr`); constants in UPPER_CASE at module top.
- States are `(row, col)` tuples; actions are the strings "UP", "DOWN", "LEFT", "RIGHT".
- Run `pytest` before declaring a task done.

## Sub-agents (Strategy 4)
Delegate focused work to the specialists in `.claude/agents/` instead of doing everything in
the main conversation:
- `environment-builder` – builds/changes `src/environment.py` only.
- `qlearning-agent` – builds/changes `src/q_learning.py` only; sees only the env interface.
- `code-reviewer` – read-only review of diffs for correctness and rule violations.
