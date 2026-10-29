# User Memory Example (`~/.claude/CLAUDE.md`)

Strategy 1 has three memory levels. Project memory (`./CLAUDE.md`) and dynamic imports
(`.claude/context/`) are in this repo. **User memory** lives in each teammate's home folder
(`~/.claude/CLAUDE.md`), applies to all of their projects, and is **not committed**,
because it holds personal preferences rather than project rules.

This is an example of what a Team 17 member might keep there:

```markdown
# Personal Development Preferences

## Code style
- Explain non-obvious lines with short comments; I am learning RL.
- Prefer small functions (under ~25 lines).

## Workflow
- Show me a plan before editing more than one file.
- Run tests before saying a task is done.
- Summaries in 3–5 bullet points.
```

You can also add to user memory from inside Claude Code with `/memory`.
