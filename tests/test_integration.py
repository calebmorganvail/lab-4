"""Integration tests: train with a fixed seed and follow the greedy policy."""

import pytest

import main as main_module
from environment import VacuumGridEnv
from main import (
    LIVING_REWARD,
    average_reward_per_block,
    build_agent,
    format_policy_grid,
    format_q_table,
    train,
)
from q_learning import QLearningAgent

PENALTY_STATE = (3, 1)
MAX_GREEDY_PATH_STEPS = 10
MIN_FINAL_AVERAGE_REWARD = 5.0


def _trained(
    terminal_states: set | None = None,
) -> tuple[VacuumGridEnv, QLearningAgent, list[float]]:
    env = VacuumGridEnv(living_reward=LIVING_REWARD)
    agent = build_agent(env)
    rewards = train(env, agent, terminal_states=terminal_states)
    return env, agent, rewards


def test_greedy_policy_reaches_goal_and_avoids_penalty() -> None:
    env, agent, _ = _trained()
    policy = agent.greedy_policy()
    state = env.reset()
    visited = [state]
    done = False
    for _ in range(MAX_GREEDY_PATH_STEPS):
        assert state in policy, f"greedy path entered state {state} with no Q-table entry"
        state, _, done = env.step(policy[state])
        visited.append(state)
        if done:
            break
    assert done, f"goal not reached within {MAX_GREEDY_PATH_STEPS} steps: {visited}"
    assert PENALTY_STATE not in visited


def test_training_is_reproducible_and_improves() -> None:
    _, _, first = _trained()
    _, _, second = _trained()
    assert first == second
    averages = average_reward_per_block(first)
    assert averages[-1] > MIN_FINAL_AVERAGE_REWARD
    assert averages[-1] > averages[0]


def test_train_records_terminal_states() -> None:
    terminal_states: set = set()
    _, agent, _ = _trained(terminal_states)
    assert len(terminal_states) == 1
    assert next(iter(terminal_states)) not in agent.q_table


def test_train_respects_step_limit() -> None:
    env = VacuumGridEnv(living_reward=LIVING_REWARD)
    agent = build_agent(env)
    train(env, agent, episodes=3, max_steps_per_episode=1)
    # One step per episode means at most one state-action pair updated per episode.
    updated = sum(
        1 for row in agent.q_table.values() for value in row.values() if value != 0.0
    )
    assert updated <= 3


def test_policy_grid_marks_unvisited_and_terminal_states() -> None:
    env = VacuumGridEnv()
    agent = build_agent(env)
    assert format_policy_grid(agent, 2, 3) == ". . .\n. . ."
    assert format_policy_grid(agent, 2, 3, {(1, 2)}) == ". . .\n. . G"


def test_policy_grid_shows_goal_after_training() -> None:
    terminal_states: set = set()
    _, agent, _ = _trained(terminal_states)
    grid = format_policy_grid(agent, 4, 4, terminal_states)
    assert grid.count("G") == 1


def test_average_reward_per_block_handles_partial_and_empty() -> None:
    assert average_reward_per_block([1.0, 3.0, 5.0], block_size=2) == [2.0, 5.0]
    assert average_reward_per_block([]) == []


def test_format_q_table_lists_every_visited_state() -> None:
    _, agent, _ = _trained()
    lines = format_q_table(agent).splitlines()
    assert len(lines) == len(agent.q_table)
    assert all("UP:" in line and "RIGHT:" in line for line in lines)


def test_main_requires_rows_and_cols(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("sys.argv", ["main.py"])
    with pytest.raises(SystemExit) as exit_info:
        main_module.main()
    assert exit_info.value.code == 2


def test_main_prints_policy(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr("sys.argv", ["main.py", "--rows", "4", "--cols", "4"])
    main_module.main()
    output = capsys.readouterr().out
    assert "Greedy policy:" in output
    assert "G" in output.split("Greedy policy:")[1]
