---
name: wt-plan
description: Trunk-phase skill for WT-PM workflow. Handles task definition dialogue, plan file creation, plan commit to trunk, worktree creation, and config sync. Run this on the trunk (dev) branch before switching to the task worktree.
user-invocable: true
---

# wt-plan: Task Planning & Worktree Setup (Trunk Phase)

Trunk-side skill for the WT-PM lifecycle. Run this from the **trunk (`dev`) branch terminal**.

Covers:
1. Pre-check: task_id conflict detection
2. Multi-round task definition dialogue
3. Update `plans/todo_current.md`
4. Create plan three-files (via `quick-plan`)
5. Commit plan artifacts to trunk
6. Create task worktree + sync shared config

For the implementation phase (worktree terminal), use `wt-dev`.

## Trigger Phrases

- `确认task`
- `task已确认`
- `写plan`
- `创建wt`
- `plan done create wt`
- `wt-plan`
- `规划并建wt`

## Runtime Parameters

Parse from user request, or derive interactively:

- `task_id` (required): e.g. `TC-107`
- `slug` (required): e.g. `receiver-mapping-ui`
- `trunk` (optional, default: `dev`)
- `worktree_path` (optional, default: `../wt-<task_id>`)
- `apply_sync` (optional, default: `true`)

Derived:
- `feature_branch = feat/<task_id>-<slug>`
- `plan_id`: from `quick-plan` output (format: `YYYYMMDD-HHmm`)

---

## Phase 0: Pre-Check（对话前置检查）

**在进入任务定义对话之前，先执行状态检查。**

目的：避免对话结束后才发现 task_id 冲突，防止重复创建已有任务的 plan。

### 0a. 确认当前分支

```bash
git branch --show-current
```

**Stop condition:** 如果当前分支不是 trunk（`dev` / `main`），停止并告知用户：
```
⚠️  当前分支是 <branch>，不是 trunk。
wt-plan 必须在 trunk 终端执行。请切换到 trunk 后重试。
```

### 0b. 如果用户已提供 task_id，立即检查状态

```bash
python ~/.claude/skills/wt-pm/scripts/plan_tracker.py --root . list
```

根据 `task_id` 的状态：

| 状态 | 行动 |
|------|------|
| 不存在 | 正常进入 Phase 1（任务定义对话） |
| `UNPLANNED` | 告知任务已存在但未规划，确认是否继续规划 |
| `PLANNED` | 询问用户：**续做已有 plan** 还是**重新规划**？<br>- 续做 → 切换到该 worktree 终端，使用 `wt-dev`<br>- 重新规划 → 确认后继续，原 plan 作废 |
| `DONE` | **停止**。告知任务已完成，不需要重新规划。|

如果用户未提供 task_id，跳过 0b，直接进入 Phase 1。

---

## Phase 1: Task Definition Dialogue（pre-commit gate）

Goal: reach shared understanding on task scope before writing anything to disk.

**When to run:**
- 如果用户说"确认task"或等效触发词，且 Phase 0 未检测到冲突，进入对话模式。
- 如果用户的请求已包含清晰的任务描述、`task_id` 和 `slug`，跳过对话直接进入 Phase 2。

**Dialogue checklist（逐一确认，直到全部回答）：**

1. Task goal: 这个任务解决什么问题？
2. Scope: 仅前端 / 仅后端 / 全栈？
3. Acceptance criteria: 如何判断完成？
4. Dependencies: 阻塞了哪些任务，或被哪些任务阻塞？
5. `task_id` 和 `slug`: 确认或提议。

全部确认后宣告："Task definition confirmed. Proceeding to plan creation."

**Stop condition:** 如果用户经过两轮对话仍无法明确验收标准，停止并要求用户先澄清后再继续。

---

## Phase 2: Update `plans/todo_current.md`

Goal: ensure task entry exists with correct status before creating plan files.

```bash
python ~/.claude/skills/wt-pm/scripts/plan_tracker.py --root . list
```

Rules:
- 如果 `task_id` 不存在：手动或通过脚本添加 `UNPLANNED` 条目，然后继续。
- 如果 `task_id` 存在且状态为 `UNPLANNED`：继续进入 Phase 3。
- 如果 `task_id` 存在且状态为 `PLANNED`：（此情况应已在 Phase 0 处理，此处再次确认）询问用户。
- 如果 `task_id` 存在且状态为 `DONE`：停止。任务已完成。

---

## Phase 3: Create Plan Three-Files

Goal: generate structured plan artifacts and bind them to the task.

```bash
python ~/.claude/skills/wt-pm/scripts/plan_tracker.py --root . quick-plan --task-ids <task_id>
```

This command:
- Creates `plans/workplans/task_plan.<plan_id>.md`
- Creates `plans/workplans/findings.<plan_id>.md`
- Creates `plans/workplans/progress.<plan_id>.md`
- Updates `plans/todo_current.md` status to `PLANNED` with `plan_id`

After running, verify three files exist under `plans/workplans/` and `todo_current.md` shows `PLANNED`.

Fill in the plan files with content from the Phase 1 dialogue:
- `task_plan.<plan_id>.md`: goal, acceptance criteria, implementation phases
- `findings.<plan_id>.md`: scope decision rationale, known dependencies, risks
- `progress.<plan_id>.md`: initial entry noting plan created, start timestamp

**Stop condition:** If any file is missing after `quick-plan`, stop and report.

---

## Phase 4: Commit Plan Artifacts to Trunk

Goal: persist planning snapshot to trunk before worktree creation.

Pre-conditions（必须全部满足）:
- 当前在 trunk 分支（`dev`）。
- 三个 plan 文件均存在且非空。
- `plans/todo_current.md` 中 `task_id` 状态为 `PLANNED`。

Commands:

```bash
git add plans/todo_current.md \
        plans/workplans/task_plan.<plan_id>.md \
        plans/workplans/findings.<plan_id>.md \
        plans/workplans/progress.<plan_id>.md
git commit -m "<task_id>: add planning docs for <slug>"
```

Rules:
- 只 stage 这四个路径。不包含其他无关变更。
- 如果任何文件缺失或未 staged，停止并列出缺失项。
- Commit 成功后进入 Phase 5。

---

## Phase 5: Create Task Worktree + Sync Config

Goal: create an isolated task branch/worktree and sync shared config files.

### 5a. Check if worktree already exists

```bash
git worktree list
```

- 如果 `../wt-<task_id>` 已存在：跳过 `git worktree add`，直接进行 sync。
- 如果不存在：执行 `git worktree add`。

### 5b. Create worktree（if new）

```bash
git worktree add -b feat/<task_id>-<slug> ../wt-<task_id> <trunk>
```

Rules:
- 默认路径：`../wt-<task_id>`（同级目录，可见）。
- 不要创建在隐藏目录（如 `.worktrees/`）下。
- 如果因权限/sandbox 限制失败，停止并报告。
- 不改变 `feat/<task_id>-<slug>` 命名约定。

### 5c. Sync shared config（dry-run then apply）

从 trunk worktree 根目录执行（同步方向：当前目录 → 任务 worktree）：

```bash
bash ~/.claude/skills/wt-pm/scripts/sync_worktree_config.sh
bash ~/.claude/skills/wt-pm/scripts/sync_worktree_config.sh --apply
```

Windows fallback（`bash` 不可用时）：

```powershell
powershell -ExecutionPolicy Bypass -File ~/.claude/skills/wt-pm/scripts/sync_worktree_config.ps1
powershell -ExecutionPolicy Bypass -File ~/.claude/skills/wt-pm/scripts/sync_worktree_config.ps1 -Apply
```

Rules:
- Dry-run 是强制的，不可跳过。
- 如果 `.sh` 和 `.ps1` 都失败，立即停止。
- 如果 `apply_sync=false`，跳过 apply 并明确报告。

### 5d. Post-check（mandatory）

验证以下内容在任务 worktree（`../wt-<task_id>`）中存在：
- `.agents/` 目录（报告文件数量）
- `.env` 文件（验证内容 hash 与 trunk 一致）
- `frontend/.env.local` 文件（验证内容 hash 与 trunk 一致）

**Output summary（required）：**
- Created branch: `feat/<task_id>-<slug>`
- Created worktree path: `../wt-<task_id>`
- Sync method: `bash` or `powershell`
- Sync dry-run result
- Sync apply result（or `skipped`）
- Post-check result: 每项 ✅ 或 ❌ 并附说明

---

## Completion

Phase 5 通过后，输出：

```
✅ wt-plan complete for <task_id>

  Branch:   feat/<task_id>-<slug>
  Worktree: ../wt-<task_id>
  Plan ID:  <plan_id>

Next step: Open a terminal in ../wt-<task_id> and say "开工" to start wt-dev.
```

---

## Safety Rules

- 禁止 `git reset --hard` 或 `git checkout -- <path>`。
- 任何 branch/worktree 变更前必须确认 dirty-tree 状态。
- Phase 4 中只 stage 四个 plan 相关路径。
- 任何阶段失败时，不继续进入下一阶段。
