# Lab 4 – Vacuum Robot with Reinforcement Learning (Team 17)

A vacuum robot must learn to reach the +10 square of the grid below. We **do not have the
transition model T or the reward function R**, so the robot will learn with **Q-learning**
(implemented in a later lab). This repository sets up the **context engineering** that an
AI coding agent (Claude Code) will use to build that agent, using:

- **Strategy 1 – Write (Persistent Memory Architecture)**
- **Strategy 4 – Isolation via Sub-Agents**

```
start   0    0    0
  0     X    0    0
  0     0    0    0
  0    -1    0   10
```

## Project structure

```
lab-4/
├── CLAUDE.md                        # S1 – Project memory (always loaded)
├── .claude/
│   ├── settings.json                # S1 – UserPromptSubmit hook → context-switcher.sh
│   ├── context/                     # S1 – Dynamic imports (loaded only when relevant)
│   │   ├── environment.md           #      grid, rewards, wall, goal (read by main session and environment-builder only)
│   │   ├── qlearning.md             #      update rule, hyperparameters, expected output
│   │   └── testing.md               #      pytest plan for env, agent and integration
│   └── agents/                      # S4 – Sub-agents (YAML frontmatter + instructions)
│       ├── environment-builder.md   #      builds src/environment.py only
│       ├── qlearning-agent.md       #      builds src/q_learning.py; instructed not to read T or R
│       └── code-reviewer.md         #      read-only review of diffs
├── scripts/
│   └── context-switcher.sh          # S1 – picks context by git branch / prompt keywords
├── docs/
│   └── user-memory-example.md       # S1 – example of ~/.claude/CLAUDE.md (user level)
├── team17.txt                       # Repository + video links for Canvas
├── requirements.txt                 # numpy and pytest for the later Q-learning lab
└── README.md
```

Planned code (written by the sub-agents in a later lab): `src/environment.py`,
`src/q_learning.py`, `src/main.py`, `tests/`.

## Strategy 1 – Write (Persistent Memory Architecture)

Memory is split into three levels, from most stable to most dynamic:

| Level | File | What we put there and why |
|---|---|---|
| Project memory | `CLAUDE.md` | Goal, the "agent never sees T or R" rule, planned architecture, code standards and which sub-agent to use. Short and always relevant; shared through git so every teammate's Claude follows the same rules. |
| User memory | `~/.claude/CLAUDE.md` (example in `docs/`) | Personal preferences (explanation style, workflow). Not committed because it differs per person. |
| Dynamic imports | `.claude/context/*.md` | Longer, task-specific details. `environment.md` is referenced from CLAUDE.md but deliberately not imported, so the Q-learning agent never sees the grid layout; qlearning.md and testing.md are injected by the hook only when relevant. |

**Hook:** `.claude/settings.json` runs `scripts/context-switcher.sh` on every prompt
(`UserPromptSubmit`). The script loads `qlearning.md` for prompts about training, Q-tables,
epsilon, rewards, etc. (or on a `qlearning*` or `agent*` branch) and `testing.md` for test/debug prompts
(or on a `test*` branch). It logs what it has already loaded in this session and never injects
the same file twice, which prevents the context bloat warned about in lecture.

## Strategy 4 – Isolation via Sub-Agents

The main Claude session acts as the **orchestrator**: it reads `CLAUDE.md`, splits the task and
delegates to specialists in `.claude/agents/`. Each sub-agent gets its own context window,
a limited set of tools and only the information it needs:

| Sub-agent | Tools | Sees | Why isolated |
|---|---|---|---|
| `environment-builder` | Read, Write, Edit, Bash, Glob | Full environment spec | Only place T and R are allowed to exist. |
| `qlearning-agent` | Read, Write, Edit, Bash | Only `reset()`, `step()`, `actions` | Mirrors the lab: the learner must not know T or R, so it is not given them. |
| `code-reviewer` | Read, Grep, Glob (read-only) | Only the diff | Focused review; checks the isolation rule was not broken. |

This addresses **context confusion** (lecture): each agent's knowledge is limited to its task,
and the Q-learning agent is instructed not to read the grid layout.

### Limits of this approach
- **Isolation here is instructed, not guaranteed.** The agents have file and shell tools, so the rules in their prompts are advisory. The code-reviewer checks that the rules were followed.
- **Cost.** Each sub-agent has its own context window, and multi-agent runs use substantially more
  tokens than a single conversation (Anthropic's multi-agent research post discusses this:
  https://www.anthropic.com/engineering/multi-agent-research-system).
- **Shared-context risk.** Cognition argues that agents working from partial context can make
  conflicting decisions (https://cognition.ai/blog/dont-build-multi-agents). We limit this by
  splitting along a clean interface (`reset`/`step`/`actions`) and keeping edits to separate files.

## How to use

1. Install [Claude Code](https://docs.claude.com/en/docs/claude-code) and `jq` (used by the hook script).
2. Install the Python dependencies for the later Q-learning lab: `pip install -r requirements.txt`
3. Open the repo: `cd lab-4 && claude`
4. Check memory and agents: `/memory` and `/agents`.
5. Example prompts:
   - `Use the environment-builder sub-agent to create the grid environment.`
   - `Use the qlearning-agent to implement Q-learning and train for 1000 episodes.` (hook loads `qlearning.md`)
   - `Use the code-reviewer to review the changes.`
