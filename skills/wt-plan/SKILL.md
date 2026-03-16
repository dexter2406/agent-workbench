---
name: wt-plan
description: Trunk-phase skill for WT-PM workflow. Handles task definition dialogue, plan file creation, plan commit to trunk, and prepares the branch/worktree handoff. Use this on the trunk branch before entering the task worktree. Do not use it for task-local environment setup.
user-invocable: true
---

# wt-plan: Task Planning & Worktree Handoff (Trunk Phase)

**REQUIRED SUB-SKILL:** Use `planning-with-files` when creating or updating WT-PM task plans.

Trunk-side skill for the WT-PM lifecycle. Run this from the **trunk (`dev`) branch terminal**.

Covers:
1. Pre-check: task_id conflict detection
2. Multi-round task definition dialogue
3. Update `plans/todo_current.md`
4. Create plan three-files (via `quick-plan`)
5. Commit plan artifacts to trunk
6. Prepare the task branch / worktree handoff

For the implementation phase (worktree terminal), use `wt-dev`.

## Plan Layering Rule

`wt-plan` 负责的是 WT-PM 的任务级 planning，不是替代仓库自己的方案级 design/implementation plan。
任务级 planning 的执行层必须使用 `planning-with-files`，不能手工绕过。

在进入 Phase 1 之前，先应用这条规则：

- 如果仓库已有 `docs/plans/` 或同类目录下的方案级 plan，先把它们作为上层输入
- `wt-plan` 通过 `planning-with-files` 生成当前 task 的 task-specific plan，落在 `plans/workplans/`
- 方案级 plan 可以指导多个 task
- task-specific plan 不得擅自偏离已批准的方案级 plan，除非用户明确要求改设计
- 如果工作很小，且用户明确不想进入 WT-PM，可不使用 `wt-plan`

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
- `worktree_path` (optional): existing path or recommended path for manual `git worktree add`

Derived:
- `feature_branch = feat/<task_id>-<slug>`
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
| `PLANNED` | 询问用户：**续做已有 task workplan** 还是**重新规划**？<br>- 续做 → 切换到该 worktree 终端，使用 `wt-dev`<br>- 重新规划 → 确认后继续，原 workplan 作废 |
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
6. Relevant higher-level plan: 是否已有方案级 plan 约束当前任务？如果有，先记录其路径和影响范围。

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

Before creating or updating these files, invoke `planning-with-files` and follow its file-based planning rules. Do not hand-write substitute planning files unless the skill is unavailable.

```bash
python ~/.claude/skills/wt-pm/scripts/plan_tracker.py --root . quick-plan --task-id <task_id>
```

This command:
- Creates `plans/workplans/<task_id>/task_plan.md`
- Creates `plans/workplans/<task_id>/findings.md`
- Creates `plans/workplans/<task_id>/progress.md`
- Updates `plans/todo_current.md` status to `PLANNED`

After `quick-plan`, continue following `planning-with-files` expectations:
- fill each file with enough structure to support session recovery
- keep findings and progress updated as work advances
- treat `plans/workplans/` as the execution memory for the task

After running, verify three files exist under `plans/workplans/` and `todo_current.md` shows `PLANNED`.

Fill in the plan files with content from the Phase 1 dialogue:
- `plans/workplans/<task_id>/task_plan.md`: goal, acceptance criteria, implementation phases
- `plans/workplans/<task_id>/findings.md`: scope decision rationale, known dependencies, risks, and any referenced higher-level plans
- `plans/workplans/<task_id>/progress.md`: initial entry noting plan created, start timestamp

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
        plans/workplans/<task_id>/task_plan.md \
        plans/workplans/<task_id>/findings.md \
        plans/workplans/<task_id>/progress.md
git commit -m "<task_id>: add planning docs for <slug>"
```

Rules:
- 只 stage 这四个路径。不包含其他无关变更。
- 如果任何文件缺失或未 staged，停止并列出缺失项。
- Commit 成功后进入 Phase 5。

---

## Phase 5: Prepare Branch / Worktree Handoff

Goal: finish trunk-side planning and hand off into a task worktree without doing task-local setup on trunk.

Required outputs:
- Feature branch name: `feat/<task_id>-<slug>`
- Existing or recommended worktree path
- Clear instruction that environment initialization must happen inside the task worktree via `wt-dev`

Rules:
- `wt-plan` must not run task-local install/setup commands on trunk.
- `wt-plan` must not assume a single creation mechanism.
- Support both of these worktree entry modes:
  - Codex app handoff using a fresh branch name
  - Manual `git worktree add`
- If the task worktree already exists, instruct the user to open that existing worktree instead of creating a second one.
- Trunk is responsible for task context only; worktree-local state belongs to the task worktree.

---

## Completion

Phase 5 通过后，输出：

```
✅ wt-plan complete for <task_id>

  Branch:   feat/<task_id>-<slug>
  Worktree: <existing path or recommended path>
Next step: Enter the task worktree using Codex app handoff or a manual git worktree, then say "开工" to start wt-dev.
```

---

## Safety Rules

- 禁止 `git reset --hard` 或 `git checkout -- <path>`。
- 任何 branch/worktree 变更前必须确认 dirty-tree 状态。
- Phase 4 中只 stage 四个 plan 相关路径。
- 不在 trunk 阶段执行 task-local install、ignored local file sync、或其他环境初始化动作。
- 任何阶段失败时，不继续进入下一阶段。
