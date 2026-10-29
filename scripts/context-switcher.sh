#!/bin/bash
# Strategy 1 (Write) – dynamic context imports.
# Runs on every UserPromptSubmit (see .claude/settings.json). Whatever this script prints
# is added to Claude's context for that prompt. It picks short, task-relevant context files
# based on the git branch and keywords in the user's prompt, and keeps a per-session record
# so the same file is never injected twice (avoids context bloat).

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
CONTEXT_DIR="$PROJECT_DIR/.claude/context"

# Fail safe: without jq the JSON on stdin cannot be parsed, so nothing would ever load.
command -v jq >/dev/null 2>&1 || { echo "context-switcher: jq not found, skipping dynamic context" >&2; exit 0; }

INPUT=$(cat)                                   # hook input is JSON on stdin
PROMPT=$(echo "$INPUT" | jq -r '.prompt // ""' 2>/dev/null)
SESSION=$(echo "$INPUT" | jq -r '.session_id // "default"' 2>/dev/null)
BRANCH=$(git -C "$PROJECT_DIR" branch --show-current 2>/dev/null)

LOADED_LOG="${TMPDIR:-/tmp}/lab4-context-$SESSION.log"
touch "$LOADED_LOG"

add_context() {
    local file="$CONTEXT_DIR/$1"
    [[ -f "$file" ]] || return
    if ! grep -qxF "$1" "$LOADED_LOG"; then     # idempotency check: skip if already loaded
        echo "$1" >> "$LOADED_LOG"
        echo "--- Context: $1 ---"
        cat "$file"
    fi
}

# Context based on git branch
case "$BRANCH" in
    qlearning*|agent*) add_context "qlearning.md" ;;
    test*)             add_context "testing.md" ;;
esac

# Context based on the user's prompt
if echo "$PROMPT" | grep -Eiqw 'q-?learning|q-?table|train(s|ed|ing)?|policy|epsilon|alpha|gamma|rewards?|episodes?'; then
    add_context "qlearning.md"
fi
if echo "$PROMPT" | grep -Eiqw 'tests?|testing|pytest|bugs?|debug(ging)?|fail(s|ed|ing|ures?)?'; then
    add_context "testing.md"
fi

exit 0
