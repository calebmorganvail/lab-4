# Lab 4 – Vacuum Robot with Reinforcement Learning (Team 17)

A vacuum robot must learn to navigate the grid below **without** being given the transition model T or the reward function R, so it will use **Q-learning** (implemented in a later lab). This lab sets up the context-engineering configuration that an AI assistant (Claude) uses to build that agent.

```
start  0   0   0
0      X   0   0
0      0   0   0
0     -1   0   10
```

## Context engineering strategies
| Strategy | Where | What it does |
|---|---|---|
| 1 – _TODO: name from lecture_ | _TODO_ | _TODO_ |
| 4 – MCP (Model Context Protocol) | `mcp_server.py`, `mcp_client.py` | Serves the project context (environment, constraints, Q-learning plan) to Claude through tools, resources and prompts |

## Project structure
```
.
├── main.py            # Entry point: starts the MCP client + CLI chat with Claude
├── mcp_server.py      # MCP server: vacuum-world docs + tools, resources, prompts
├── mcp_client.py      # MCP client: list/call tools, list/get prompts, read resources
├── core/              # Provided chat app (Claude wrapper, CLI, tool handling)
├── pyproject.toml     # Dependencies
├── uv.lock
├── .env.example       # Copy to .env and add your API key
└── README.md
```

### MCP server contents
- **Documents:** `environment.md` (grid, rewards, actions), `constraints.md` (T and R unknown → model-free), `qlearning_plan.md` (update rule, hyperparameters)
- **Tools** (Claude decides when to call): `read_doc_contents`, `edit_document`
- **Resources** (`@mention` in chat): `docs://documents`, `docs://documents/{doc_id}`
- **Prompts** (`/command` in chat): `/format`, `/summarize`, `/plan_qlearning`

## Setup and run
```bash
cp .env.example .env        # then add your ANTHROPIC_API_KEY
uv venv && source .venv/bin/activate
uv pip install -e .
uv run main.py
```
Try: `Tell me about @environment.md` or `/plan_qlearning environment.md`

Test the server alone: `uv run mcp dev mcp_server.py` (inspector at http://127.0.0.1:6274), or `uv run mcp_client.py`.
