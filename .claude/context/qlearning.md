# Q-Learning Context (loaded on demand)

Loaded by `scripts/context-switcher.sh` when the prompt mentions Q-learning, training,
policy, reward, epsilon, etc., or when working on a `qlearning*` branch.

## Why Q-learning
T and R are unknown, so model-based methods (value/policy iteration) cannot be used.
Q-learning is model-free and off-policy: it learns Q(s, a) directly from sampled transitions.

## Update rule
Q(s, a) <- Q(s, a) + alpha * [ r + gamma * max_a' Q(s', a') - Q(s, a) ]
For a terminal s', use max_a' Q(s', a') = 0.

## Starting hyperparameters (tune and document changes)
| Name | Value | Meaning |
|------|-------|---------|
| learning_rate (alpha) | 0.1 | how much each sample moves Q |
| discount_factor (gamma) | 0.9 | value of future reward |
| epsilon | 1.0 -> 0.05, decay 0.995/episode | exploration rate (epsilon-greedy) |
| episodes | 1000 | training episodes |
| max_steps_per_episode | 100 | prevents endless wandering |

## Expected outputs
- Final Q-table (16 states x 4 actions, wall row unused).
- Greedy policy printed as arrows on the 4x4 grid.
- Total reward per episode (to show learning converges).
