# Project Memory – Vacuum Robot Q-Learning (CS440 Lab 4, Team 17)

<!-- Strategy 1 (Write): project-level persistent memory. Loaded every session and shared
     with the whole team through git. Keep it short and always-relevant; longer, task-specific
     context lives in .claude/context/ and is loaded on demand. -->

## Goal
Build a vacuum robot agent that learns to reach the goal square of a 4x4 grid world using
**Q-learning**. The agent is NOT given the transition model T or the reward function R.

## Core environment
Environment details live in `.claude/context/environment.md`. Only the main session and
`environment-builder` should read it. `qlearning-agent` must not.

## Non-negotiable rules
- The learner (`src/q_learning.py`, `src/main.py`) must never read T, R or the grid layout directly.
  It only interacts through `VacuumGridEnv()`, `env.reset()`, `env.actions` and
  `env.step(action) -> (next_state, reward, done)`.
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


### Delegation rules (keep the isolation intact)
- When delegating to `qlearning-agent`, pass only the task and the public interface
  (`VacuumGridEnv()`, `reset()`, `step()`, `actions`). Never paste the grid layout, wall,
  penalty or goal positions into its prompt.
- When delegating to `code-reviewer`, paste the diff into the prompt (it has no shell to run `git diff`).
- Integration tests (`tests/test_integration.py`) are written by the main session, not by a sub-agent.