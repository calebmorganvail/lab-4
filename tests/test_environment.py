"""Tests for the vacuum grid environment."""

import pytest

from environment import DEFAULT_LIVING_REWARD, VacuumGridEnv


@pytest.fixture
def env() -> VacuumGridEnv:
    environment = VacuumGridEnv()
    environment.reset()
    return environment


def walk(env: VacuumGridEnv, moves: list[str]) -> tuple[tuple[int, int], float, bool]:
    result = None
    for move in moves:
        result = env.step(move)
    return result


def test_reset_returns_start() -> None:
    assert VacuumGridEnv().reset() == (0, 0)


def test_actions() -> None:
    assert VacuumGridEnv().actions == ["UP", "DOWN", "LEFT", "RIGHT"]


def test_normal_move_gives_living_reward(env: VacuumGridEnv) -> None:
    assert env.step("RIGHT") == ((0, 1), DEFAULT_LIVING_REWARD, False)


def test_edge_keeps_robot_in_place(env: VacuumGridEnv) -> None:
    assert env.step("UP") == ((0, 0), DEFAULT_LIVING_REWARD, False)
    assert env.step("LEFT") == ((0, 0), DEFAULT_LIVING_REWARD, False)


def test_wall_blocks_movement(env: VacuumGridEnv) -> None:
    env.step("RIGHT")                        # (0, 1)
    state, _, _ = env.step("DOWN")           # (1, 1) is the wall
    assert state == (0, 1)


def test_penalty_square(env: VacuumGridEnv) -> None:
    state, reward, done = walk(env, ["DOWN", "DOWN", "DOWN", "RIGHT"])
    assert (state, reward, done) == ((3, 1), -1.0, False)


def test_goal_is_terminal(env: VacuumGridEnv) -> None:
    state, reward, done = walk(env, ["RIGHT", "RIGHT", "DOWN", "DOWN", "DOWN", "RIGHT"])
    assert (state, reward, done) == ((3, 3), 10.0, True)


def test_step_after_goal_raises(env: VacuumGridEnv) -> None:
    walk(env, ["RIGHT", "RIGHT", "DOWN", "DOWN", "DOWN", "RIGHT"])
    with pytest.raises(RuntimeError):
        env.step("UP")
    assert env.reset() == (0, 0)


def test_invalid_action(env: VacuumGridEnv) -> None:
    with pytest.raises(ValueError):
        env.step("JUMP")


def test_custom_living_reward() -> None:
    env = VacuumGridEnv(living_reward=-0.5)
    env.reset()
    assert env.step("RIGHT")[1] == -0.5
