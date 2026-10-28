from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base
from pydantic import Field

mcp = FastMCP("VacuumRL_MCP", log_level="ERROR")

# Context documents for the Lab 4 vacuum robot (Q-learning) project.
# These are served to Claude through MCP tools, resources and prompts.
docs = {
    "environment.md": """# Vacuum World Environment (Lab 4)
4x4 grid. Rows/cols are 0-indexed, (row, col), origin at top-left.

| r\\c | 0     | 1  | 2 | 3  |
|-----|-------|----|---|----|
| 0   | start | 0  | 0 | 0  |
| 1   | 0     | X  | 0 | 0  |
| 2   | 0     | 0  | 0 | 0  |
| 3   | 0     | -1 | 0 | 10 |

- start: (0,0), reward 0
- X: (1,1) is a wall / obstacle; the robot cannot enter it (it stays in place)
- -1 at (3,1): penalty square
- 10 at (3,3): goal, terminal state
- All other squares: reward 0
- Actions: UP, DOWN, LEFT, RIGHT. Moving into a wall or off-grid leaves the robot in place.
""",
    "constraints.md": """# Project Constraints
- The agent is NOT given the transition model T(s, a, s') or the reward function R(s).
- It must learn only from experience: (state, action, reward, next_state) samples.
- Therefore use model-free learning: Q-learning (implementation comes in a later lab).
- The environment simulator may know the grid, but the agent may only call env.step(action).
""",
    "qlearning_plan.md": """# Q-learning Plan (to implement later)
Update rule: Q(s,a) <- Q(s,a) + alpha * (r + gamma * max_a' Q(s',a') - Q(s,a))
Proposed hyperparameters (to tune): alpha=0.1, gamma=0.9, epsilon=0.1 (epsilon-greedy),
episodes=1000, episode ends at the goal (3,3) or after a max step limit.
Output: learned Q-table and the greedy policy printed as arrows on the grid.
""",
}


def _get_doc(doc_id: str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    return docs[doc_id]


# ---------- Tools (Claude decides when to call) ----------
@mcp.tool(
    name="read_doc_contents",
    description="Read the contents of a document and return it as a string.",
)
def read_document(doc_id: str = Field(description="Id of the document to read")):
    return _get_doc(doc_id)


@mcp.tool(
    name="edit_document",
    description="Edit a document by replacing a string in the document's content with a new string.",
)
def edit_document(
    doc_id: str = Field(description="Id of the document that will be edited"),
    old_str: str = Field(description="The text to replace. Must match exactly, including whitespace"),
    new_str: str = Field(description="The new text to insert in place of the old text"),
):
    _get_doc(doc_id)
    docs[doc_id] = docs[doc_id].replace(old_str, new_str)
    return f"Updated {doc_id}"


# ---------- Resources (app injects data via @mentions) ----------
@mcp.resource("docs://documents", mime_type="application/json")
def list_docs() -> list[str]:
    return list(docs.keys())


@mcp.resource("docs://documents/{doc_id}", mime_type="text/plain")
def fetch_doc(doc_id: str) -> str:
    return _get_doc(doc_id)


# ---------- Prompts (user runs as /commands) ----------
@mcp.prompt(name="format", description="Rewrites the contents of the document in Markdown format.")
def format_document(doc_id: str = Field(description="Id of the document to format")) -> list[base.Message]:
    prompt = f"""Your goal is to reformat a document to be written with markdown syntax.
The id of the document you need to reformat is: <document_id>{doc_id}</document_id>
Add headers, bullet points, tables, etc. as necessary. Feel free to add in extra text, but don't change the meaning.
Use the 'edit_document' tool to edit the document. After the document has been edited, respond with the final version."""
    return [base.UserMessage(prompt)]


@mcp.prompt(name="summarize", description="Summarizes the contents of the document.")
def summarize_document(doc_id: str = Field(description="Id of the document to summarize")) -> list[base.Message]:
    prompt = f"""Read the document with id <document_id>{doc_id}</document_id> using the
'read_doc_contents' tool and write a concise summary of it."""
    return [base.UserMessage(prompt)]


@mcp.prompt(
    name="plan_qlearning",
    description="Uses the project docs to explain how the Q-learning agent should be built for this environment.",
)
def plan_qlearning(doc_id: str = Field(description="Id of the doc to focus on, e.g. environment.md")) -> list[base.Message]:
    prompt = f"""You are helping build a vacuum robot that learns with Q-learning.
First read 'environment.md', 'constraints.md' and 'qlearning_plan.md' with the 'read_doc_contents' tool
(focus especially on {doc_id}). Then describe the states, actions, rewards and terminal state,
explain why T and R are unknown to the agent, and outline the Q-learning code structure.
Do not assume access to T or R inside the agent."""
    return [base.UserMessage(prompt)]


if __name__ == "__main__":
    mcp.run(transport="stdio")
