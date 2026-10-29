# Environment Specification – Vacuum Grid World

4x4 grid, coordinates are `(row, col)`, 0-indexed, `(0, 0)` is the top-left.

| row\col | 0     | 1      | 2 | 3       |
|---------|-------|--------|---|---------|
| 0       | START | 0      | 0 | 0       |
| 1       | 0     | X wall | 0 | 0       |
| 2       | 0     | 0      | 0 | 0       |
| 3       | 0     | -1     | 0 | +10 GOAL|

- **Start:** `(0, 0)`
- **Wall:** `(1, 1)` cannot be entered; moving into it leaves the robot where it is.
- **Penalty:** entering `(3, 1)` gives reward -1 (not terminal).
- **Goal:** entering `(3, 3)` gives reward +10 and ends the episode (terminal).
- **All other moves:** reward 0.
- **Actions:** UP, DOWN, LEFT, RIGHT. Moving off the grid leaves the robot in place.
- **Transitions:** deterministic. The same action in the same state always gives the same result.
- **After the goal:** calling `step()` after `done=True` raises `RuntimeError` until `reset()` is called.
- **Unknowns:** the agent does not know T or R in advance; it must learn from experience.
