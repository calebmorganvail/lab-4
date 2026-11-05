"""Unit tests for QLearningAgent using made-up states."""

import pytest

from q_learning import QLearningAgent

ACTIONS = ["UP", "DOWN", "LEFT", "RIGHT"]


def make_agent(**kwargs) -> QLearningAgent:
    return QLearningAgent(ACTIONS, seed=0, **kwargs)


def test_new_state_starts_at_zero() -> None:
    agent = make_agent()
    assert agent.get_q_values((5, 7)) == {a: 0.0 for a in ACTIONS}
    assert (5, 7) in agent.q_table


def test_update_matches_hand_computation() -> None:
    agent = make_agent(learning_rate=0.5, discount_factor=0.9)
    agent.get_q_values((5, 7))["LEFT"] = 2.0  # max of next state
    agent.get_q_values((0, 0))["UP"] = 1.0
    new_value = agent.update((0, 0), "UP", -1.0, (5, 7), False)
    # 1.0 + 0.5 * (-1 + 0.9*2.0 - 1.0) = 1.0 + 0.5 * (-0.2) = 0.9
    assert new_value == pytest.approx(0.9)
    assert agent.q_table[(0, 0)]["UP"] == pytest.approx(0.9)
    assert agent.q_table[(0, 0)]["DOWN"] == 0.0


def test_terminal_update_ignores_next_state() -> None:
    agent = make_agent(learning_rate=0.1)
    new_value = agent.update((0, 0), "RIGHT", 10.0, (9, 9), True)
    assert new_value == pytest.approx(1.0)
    assert (9, 9) not in agent.q_table


def test_epsilon_zero_always_argmax() -> None:
    agent = make_agent(epsilon=0.0, epsilon_min=0.0)
    agent.get_q_values((2, 3))["LEFT"] = 0.5
    assert all(agent.choose_action((2, 3)) == "LEFT" for _ in range(200))


def test_epsilon_one_picks_every_action() -> None:
    agent = make_agent(epsilon=1.0)
    seen = {agent.choose_action((0, 0)) for _ in range(200)}
    assert seen == set(ACTIONS)


def test_epsilon_decays_but_not_below_min() -> None:
    agent = make_agent(epsilon=1.0, epsilon_min=0.05, epsilon_decay=0.5)
    assert agent.decay_epsilon() == pytest.approx(0.5)
    previous = agent.epsilon
    for _ in range(50):
        current = agent.decay_epsilon()
        assert current <= previous
        assert current >= 0.05
        previous = current
    assert agent.epsilon == pytest.approx(0.05)


def test_same_seed_same_actions() -> None:
    first = QLearningAgent(ACTIONS, seed=42)
    second = QLearningAgent(ACTIONS, seed=42)
    states = [(i % 3, i % 5) for i in range(100)]
    assert [first.choose_action(s) for s in states] == [
        second.choose_action(s) for s in states
    ]


@pytest.mark.parametrize(
    "kwargs",
    [
        {"learning_rate": 0.0},
        {"learning_rate": 1.5},
        {"discount_factor": -0.1},
        {"discount_factor": 1.1},
        {"epsilon": 1.5},
        {"epsilon": -0.1},
        {"epsilon_min": -0.1},
        {"epsilon": 0.1, "epsilon_min": 0.5},
        {"epsilon_decay": 0.0},
        {"epsilon_decay": 1.1},
    ],
)
def test_invalid_hyperparameters_raise(kwargs: dict) -> None:
    with pytest.raises(ValueError):
        QLearningAgent(ACTIONS, **kwargs)


def test_empty_actions_raise() -> None:
    with pytest.raises(ValueError):
        QLearningAgent([])


def test_unknown_action_raises() -> None:
    agent = make_agent()
    with pytest.raises(ValueError):
        agent.update((0, 0), "JUMP", 1.0, (0, 1), False)


def test_greedy_policy_is_argmax_per_state() -> None:
    agent = make_agent()
    agent.get_q_values((0, 0))["DOWN"] = 1.0
    agent.get_q_values((5, 7))["RIGHT"] = 3.0
    agent.get_q_values((5, 7))["UP"] = -1.0
    agent.get_q_values((4, 4))  # all ties -> first action
    assert agent.greedy_policy() == {
        (0, 0): "DOWN",
        (5, 7): "RIGHT",
        (4, 4): "UP",
    }
