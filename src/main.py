"""Train the vacuum robot with Q-learning and print the Q-table and greedy policy.

The learner only talks to the environment through ``reset()``, ``step()`` and
``actions``; it never reads the transition model, rewards or grid layout.
"""

from __future__ import annotations

import argparse
from typing import Hashable

from environment import VacuumGridEnv
from q_learning import QLearningAgent

RANDOM_SEED: int = 17
LIVING_REWARD: float = -0.04
DISCOUNT_FACTOR: float = 0.9
LEARNING_RATE: float = 0.1
EPSILON_START: float = 1.0
EPSILON_MIN: float = 0.05
EPSILON_DECAY: float = 0.995
EPISODES: int = 1000
MAX_STEPS_PER_EPISODE: int = 100
REPORT_INTERVAL: int = 100

ARROWS: dict[str, str] = {"UP": "^", "DOWN": "v", "LEFT": "<", "RIGHT": ">"}
UNVISITED_SYMBOL: str = "."
TERMINAL_SYMBOL: str = "G"

State = Hashable


def train(
    env: VacuumGridEnv,
    agent: QLearningAgent,
    episodes: int = EPISODES,
    max_steps_per_episode: int = MAX_STEPS_PER_EPISODE,
    terminal_states: set[State] | None = None,
) -> list[float]:
    """Run Q-learning for the given number of episodes.

    If terminal_states is given, every state where the environment reported
    done is added to it (the agent never stores terminal states in its Q-table).

    Returns:
        The total reward collected in each episode.
    """
    episode_rewards: list[float] = []
    for _ in range(episodes):
        state = env.reset()
        total_reward = 0.0
        for _ in range(max_steps_per_episode):
            action = agent.choose_action(state)
            next_state, reward, done = env.step(action)
            agent.update(state, action, reward, next_state, done)
            total_reward += reward
            state = next_state
            if done:
                if terminal_states is not None:
                    terminal_states.add(next_state)
                break
        agent.decay_epsilon()
        episode_rewards.append(total_reward)
    return episode_rewards


def average_reward_per_block(
    episode_rewards: list[float], block_size: int = REPORT_INTERVAL
) -> list[float]:
    """Average the episode rewards over consecutive blocks of episodes."""
    blocks = [
        episode_rewards[start : start + block_size]
        for start in range(0, len(episode_rewards), block_size)
    ]
    return [sum(block) / len(block) for block in blocks]


def format_q_table(agent: QLearningAgent) -> str:
    """Format the Q-table, one line per visited state, sorted by state."""
    lines = []
    for state in sorted(agent.q_table):
        values = ", ".join(
            f"{action}: {agent.q_table[state][action]:.3f}" for action in agent.actions
        )
        lines.append(f"{state}: {{{values}}}")
    return "\n".join(lines)


def format_policy_grid(
    agent: QLearningAgent,
    rows: int,
    cols: int,
    terminal_states: set[State] | None = None,
) -> str:
    """Draw the greedy policy as arrows.

    Terminal states print 'G'; states without a Q-table entry print '.'.
    """
    policy = agent.greedy_policy()
    terminal = terminal_states or set()
    lines = []
    for row in range(rows):
        cells = []
        for col in range(cols):
            if (row, col) in terminal:
                cells.append(TERMINAL_SYMBOL)
            elif (row, col) in policy:
                cells.append(ARROWS[policy[(row, col)]])
            else:
                cells.append(UNVISITED_SYMBOL)
        lines.append(" ".join(cells))
    return "\n".join(lines)


def parse_arguments() -> argparse.Namespace:
    """Parse the required display-only grid dimensions."""
    parser = argparse.ArgumentParser(description="Train the vacuum robot with Q-learning.")
    parser.add_argument("--rows", type=int, required=True, help="grid rows (display only)")
    parser.add_argument("--cols", type=int, required=True, help="grid columns (display only)")
    arguments = parser.parse_args()
    if arguments.rows < 1 or arguments.cols < 1:
        parser.error("--rows and --cols must be positive")
    return arguments


def build_agent(env: VacuumGridEnv) -> QLearningAgent:
    """Create the agent with this module's hyperparameters and fixed seed."""
    return QLearningAgent(
        env.actions,
        learning_rate=LEARNING_RATE,
        discount_factor=DISCOUNT_FACTOR,
        epsilon=EPSILON_START,
        epsilon_min=EPSILON_MIN,
        epsilon_decay=EPSILON_DECAY,
        seed=RANDOM_SEED,
    )


def main() -> None:
    """Train the agent and print hyperparameters, learning curve, Q-table and policy."""
    arguments = parse_arguments()
    env = VacuumGridEnv(living_reward=LIVING_REWARD)
    agent = build_agent(env)
    terminal_states: set[State] = set()
    episode_rewards = train(env, agent, terminal_states=terminal_states)

    print(
        f"Hyperparameters: seed={RANDOM_SEED}, living_reward={LIVING_REWARD}, "
        f"gamma={DISCOUNT_FACTOR}, alpha={LEARNING_RATE}, epsilon={EPSILON_START}->"
        f"{EPSILON_MIN} (decay {EPSILON_DECAY}), episodes={EPISODES}, "
        f"max_steps={MAX_STEPS_PER_EPISODE}"
    )
    print("\nAverage reward per block of episodes:")
    for index, average in enumerate(average_reward_per_block(episode_rewards)):
        first = index * REPORT_INTERVAL + 1
        last = min((index + 1) * REPORT_INTERVAL, len(episode_rewards))
        print(f"  episodes {first}-{last}: {average:.3f}")
    print("\nQ-table:")
    print(format_q_table(agent))
    print("\nGreedy policy:")
    print(format_policy_grid(agent, arguments.rows, arguments.cols, terminal_states))


if __name__ == "__main__":
    main()
