---
name: cross-worktree-sync
description: Read committed files and recent history from other task branches. Use when checking parallel task status, reviewing completed tasks, or syncing implementation patterns. Trigger phrases include "查看其他任务状态", "sync with task branch", and "check other branch".
user-invokable: true
---

# Cross-Worktree Sync

Read committed files and recent history from other task branches without switching away from the current worktree.

## Purpose

Use this skill when you need to inspect another task branch for status, implementation patterns, or plan evidence. This skill is read-only. It does not make decisions or edit files.

## Workflow

### 1. Determine current task

```bash
git rev-parse --abbrev-ref HEAD
```

- `feat/<task_id>-*` means the current task is `<task_id>`
- `main` or `dev` means you are on trunk
- If the branch cannot be inferred, ask the user to name the target branch

### 2. Discover other task branches

```bash
git branch --list 'feat/*'
git for-each-ref --sort=-committerdate refs/heads/feat/ --format='%(refname:short) %(committerdate:relative)'
```

Record:
- target branch name, such as `feat/TC-006-log-improve`
- target HEAD commit, using `git rev-parse --short <branch>`

### 3. Read committed files

Read files directly from the other branch:

```bash
git show <branch>:<filepath>
```

Common targets:
- `plans/workplans/progress.<plan_id>.md`
- `plans/workplans/findings.<plan_id>.md`
- `AGENTS.md`
- `CLAUDE.md`
- any committed code file the caller requests

Useful supporting commands:

```bash
git log --oneline -N <branch>
git diff <my-branch>...<other-branch> -- <filepath>
```

### 4. Output

Return:

```text
Target branch: <branch-name>
Target HEAD: <short-hash> (<commit-date>)

--- Requested file content ---
<file content>
```

## Safety Rules

- Read-only only. Do not modify files.
- Do not infer status or recommend decisions unless the caller explicitly asks for analysis outside this skill.
- Prefer committed content over working-tree content from other branches.
