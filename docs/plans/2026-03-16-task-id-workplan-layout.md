# Task-ID Workplan Layout Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Replace `plan_id`-based workplan files with a per-task directory layout keyed only by `task_id`.

**Architecture:** Refactor `plan_tracker.py` so `task_id` is the single identifier for lifecycle state and workplan storage. Update WT-PM and planning docs to point at `plans/workplans/<task_id>/` with fixed filenames and single-task planning semantics.

**Tech Stack:** Python 3, pytest, Markdown skill docs

---

### Task 1: Lock the New Tracker Behavior with Tests

**Files:**
- Create: `tests/test_plan_tracker.py`
- Modify: `skills/wt-pm/scripts/plan_tracker.py`

**Step 1: Write the failing test**

Cover:
- `quick-plan --task-ids TC-001` creates `plans/workplans/TC-001/task_plan.md`, `findings.md`, `progress.md`
- `todo_current.md` no longer requires or emits `plan_id`
- `quick-resume --task-id TC-001` prints the per-task file paths
- `set-status --task-id TC-001 --status DONE` works without `--plan-id`

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_plan_tracker.py -q`

Expected: FAIL because tracker still expects `plan_id` and flat filenames.

**Step 3: Write minimal implementation**

Refactor parser, renderer, and command handlers in `skills/wt-pm/scripts/plan_tracker.py`.

**Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_plan_tracker.py -q`

Expected: PASS.

### Task 2: Update WT-PM Documentation

**Files:**
- Modify: `skills/planning-with-files/SKILL.md`
- Modify: `skills/wt-plan/SKILL.md`
- Modify: `skills/wt-dev/SKILL.md`
- Modify: `skills/wt-pm/SKILL.md`
- Modify: `skills/wt-pm/references/wt-pm-workflow.md`
- Modify: `skills/wt-pm/rules/planning-with-files.md`
- Modify: `skills/wt-pm/rules/collaboration-boundaries.md`
- Modify: `skills/wt-pm/rules/dod-and-safety.md`
- Modify: `skills/wt-pm/templates/workplans-README.md`

**Step 1: Update terminology**

Replace `plan_id` language with `task_id` as the sole workplan identifier.

**Step 2: Update filesystem examples**

Every example should use `plans/workplans/<task_id>/task_plan.md`, `findings.md`, `progress.md`.

**Step 3: Remove multi-task planning semantics**

`quick-plan` becomes single-task only; docs should say one task maps to one workplan directory and one active worktree.

**Step 4: Verify doc consistency**

Run: `Get-ChildItem -Recurse -File skills | Select-String -Pattern 'plan_id|task_plan\\.|findings\\.|progress\\.|quick-plan --max-tasks|bind-task|quick-resume \\[--plan-id'`

Expected: no remaining references to removed concepts in WT-PM docs.

### Task 3: Final Verification

**Files:**
- Verify tracker and docs only

**Step 1: Run focused tests**

Run: `python -m pytest tests/test_plan_tracker.py -q`

**Step 2: Run doc grep**

Run: `Get-ChildItem -Recurse -File skills | Select-String -Pattern 'plan_id|quick-plan --max-tasks|bind-task|task_plan\\.[^m]|findings\\.[^m]|progress\\.[^m]'`

**Step 3: Summarize residual risks**

Call out that existing repositories must update `plans/todo_current.md` to the new schema before using the tracker.
