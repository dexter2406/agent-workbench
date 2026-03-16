#!/bin/bash
# Check if all phases in the active task_plan.md are complete
# Always exits 0 — uses stdout for status reporting
# Used by Stop hook to report task completion status

PLAN_FILE="${1:-}"

if [ -z "$PLAN_FILE" ]; then
    if [ -f "task_plan.md" ]; then
        PLAN_FILE="task_plan.md"
    else
        PLAN_FILE="$(find plans/workplans -type f -name task_plan.md 2>/dev/null | head -n 1)"
    fi
fi

if [ -z "$PLAN_FILE" ] || [ ! -f "$PLAN_FILE" ]; then
    echo "[planning-with-files] No task_plan.md found — no active planning session."
    exit 0
fi

# Count total phases
TOTAL=$(grep -c "### Phase" "$PLAN_FILE" || true)

# Check for **Status:** format first
COMPLETE=$(grep -cF "**Status:** complete" "$PLAN_FILE" || true)
IN_PROGRESS=$(grep -cF "**Status:** in_progress" "$PLAN_FILE" || true)
PENDING=$(grep -cF "**Status:** pending" "$PLAN_FILE" || true)

# Fallback: check for [complete] inline format if **Status:** not found
if [ "$COMPLETE" -eq 0 ] && [ "$IN_PROGRESS" -eq 0 ] && [ "$PENDING" -eq 0 ]; then
    COMPLETE=$(grep -c "\[complete\]" "$PLAN_FILE" || true)
    IN_PROGRESS=$(grep -c "\[in_progress\]" "$PLAN_FILE" || true)
    PENDING=$(grep -c "\[pending\]" "$PLAN_FILE" || true)
fi

# Default to 0 if empty
: "${TOTAL:=0}"
: "${COMPLETE:=0}"
: "${IN_PROGRESS:=0}"
: "${PENDING:=0}"

# Report status (always exit 0 — incomplete task is a normal state)
if [ "$COMPLETE" -eq "$TOTAL" ] && [ "$TOTAL" -gt 0 ]; then
    echo "[planning-with-files] ALL PHASES COMPLETE ($COMPLETE/$TOTAL)"
else
    echo "[planning-with-files] Task in progress ($COMPLETE/$TOTAL phases complete)"
    if [ "$IN_PROGRESS" -gt 0 ]; then
        echo "[planning-with-files] $IN_PROGRESS phase(s) still in progress."
    fi
    if [ "$PENDING" -gt 0 ]; then
        echo "[planning-with-files] $PENDING phase(s) pending."
    fi
fi
exit 0
