---
name: train-and-report
description: Trains the vacuum robot Q-learning agent, runs the tests, and reports the hyperparameters, learned policy and results. Use when asked to train, run, evaluate or demo the robot, or to report how the chosen hyperparameters performed.
allowed-tools: Read, Grep, Bash
---

# Train and Report – Vacuum Robot Q-Learning

A repeatable procedure for running the project end to end and producing the same report every
time (used for the demo and the video). This skill only **runs** the code and reports on it;
it does not write or change source files.

## Steps

1. **Check the code exists.** Confirm `src/environment.py`, `src/q_learning.py` and
   `src/main.py` exist. If any is missing, stop and say which one, and which sub-agent builds it
   (see `CLAUDE.md`).
2. **Install dependencies if needed:** `pip install -r requirements.txt`
3. **Run the tests:** `pytest -q`
   - If any test fails, stop. Report the failing test names and the error, and do not train.
4. **Train:** `python src/main.py` with its fixed random seed. Capture the full output.
5. **Read the hyperparameters** from the constants at the top of `src/main.py`
   (living reward, discount factor, learning rate, epsilon and its decay, episodes).
   Read them; do not change them.

## Report format

Reply with exactly these sections:

### Hyperparameters
| Name | Value |
|---|---|
| Living reward | … |
| Discount factor (gamma) | … |
| Learning rate (alpha) | … |
| Epsilon (start → min, decay) | … |
| Episodes | … |

### Learned policy
The greedy policy as printed by `src/main.py` (arrows on the grid), in a code block.

### Results
- Tests: X passed / Y failed
- Average reward over the last 100 episodes
- Does the greedy path from the start reach the goal? How many steps?
- Does it avoid the penalty square?

### Notes
1–3 bullets on anything unexpected (e.g. policy loops, slow convergence), with a suggested
hyperparameter change if the policy is not reaching the goal.

## Rules
- Do not edit any files. If something needs fixing, report it and suggest which sub-agent
  should fix it.
- Do not read `.claude/context/environment.md`; report only what the program outputs.
