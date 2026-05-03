# Continuous Learning 本地化与审批流改造计划

## 目标对齐

- Continuous Learning 仅在 `agent-workbench` 仓库内产出内容，不再直接在全局目录生成 Skill。
- 先把当前 Continuous Learning 方案整体纳入 `agent-workbench` 管控，再通过 install 链接到全局目录使用。
- 产出 `pending proposal` 后必须主动告知你，避免“后台静默生成”。
- 只有你审批通过后，才正式生成 Skill，并自动走现有 install 流程安装到全局。
- 按你的要求移除“阶段4：登记来源”，不新增额外 registry 账本。

## 设计结论（先答你关心点）

- 你问“写完 pending proposal 后能不能主动告诉我”：可以。
- 方案采用“结构化状态沉淀”：
  - **强制通道（必有）**：写入仓库内 `pending` 队列文件（可追溯，永不丢）。
  - **AI 必读状态文件**：每次 Hook 更新统一的结构化状态（例如 `pending/state.json`）。
- 不依赖桌面通知或终端提示，改为让 AI 在下一次任务开始时先读取状态并主动提出处理 pending。
- 关于你问的“会不会进实时聊天对话”：
  - 默认不会直接进入当前 AI 对话消息流。
  - 可感知位置改为仓库内结构化状态文件与 pending 清单。
  - Hook 的标准输出通常在宿主进程上下文里，不等同于你当前可见聊天窗口。
  - 因此流程里会把“state.json + pending 清单落盘”设为主告知通道。

## 目录与状态模型

- 新增目录（仓库内）：
  - `skills/continuous-learning/pending/`：待审批提案（`*.md` 或 `*.json`）。
  - `skills/continuous-learning/scripts/`：审批与安装脚本。
- 状态流转：
  - `detected` -> `pending` -> `approved|rejected`
- 约束：
  - `pending` 阶段禁止写 `skills/<new-skill>/`。
  - 仅 `approved` 动作可生成正式 Skill。

## 实施步骤

1. 先完成 Continuous Learning 的本地化迁移（纳入 workbench）
   - 以仓库内 `skills/continuous-learning/` 作为唯一受管控源。
   - 对齐 install 后的全局目录应为链接目标，不再依赖外部散落版本。
   - 验证 `~/.claude/skills/continuous-learning` 与 `~/.codex/skills/continuous-learning` 指向仓库路径。

2. 扩展 `continuous-learning` 配置项（仅本 skill 内）
   - 增加仓库根路径、pending 目录、通知开关、通知方式优先级。
   - 保留现有阈值配置，避免行为回归。

3. 重构 Stop Hook 执行逻辑（`evaluate-session.sh`）
   - 保留“是否值得提取”判定。
   - 命中后只生成 `pending proposal` 文件（含标题、摘要、候选名称、来源片段、时间戳）。
   - 禁止在该脚本内直接产出正式 Skill。

4. 增加“结构化可感知”能力（不依赖通知）
   - Hook 成功落 `pending` 后，同时更新 `pending/state.json`。
   - `state.json` 至少包含：
     - `hasPending`（布尔）
     - `pendingCount`
     - `latestProposal`
     - `updatedAt`
     - `nextAction`（建议执行 approve/reject/list）
   - 增加 `pending/index.json` 作为收件箱索引，记录全部待审批提案元数据。

5. 增加“下一次任务启动前必读”机制
   - 在会话启动入口或任务前置检查中，先读取 `pending/state.json`。
   - 若 `hasPending=true`，AI 先主动提示“发现待审批提案”，并给出可执行选项（approve/reject/list/skip）。
   - 仅在用户明确选择后再继续常规任务执行。

6. 新增审批命令脚本（本地人工触发）
   - `approve-pending-skill`：读取提案 -> 生成 `skills/<name>/SKILL.md`（按模板）-> 调用安装流程。
   - `reject-pending-skill`：直接删除对应 pending 提案，不生成 Skill。
   - `list-pending-skills`：查看所有待审批提案与时间。

7. 接入自动安装（审批后）
   - 审批通过后调用仓库既有安装脚本（Windows 走 `install.ps1`，Unix 走 `install.sh`）。
   - 只在审批通过后触发安装，确保“先审批后发布”。

8. 文档更新
   - 更新 `skills/continuous-learning/SKILL.md`：说明新审批流、通知机制、命令示例。
   - 补充“常见问题”：为什么看不到即时通知、如何从 `pending` 文件找回。

9. 回归验证
   - 用样例 transcript 触发 Hook：
     - 验证会生成 pending 文件。
     - 验证会发主动通知（至少有终端提示）。
   - 执行 approve：
     - 验证正式 Skill 写入仓库。
     - 验证 install 后在 `~/.claude/skills` 与 `~/.codex/skills` 可见链接。
   - 执行 reject：
     - 验证不会生成正式 Skill，且 pending 文件被删除。

## 验收标准

- 触发学习事件后，仓库内出现新的 `pending proposal`，且不会直接出现正式 Skill。
- 触发后 `pending/state.json` 与 `pending/index.json` 会同步更新，AI 下次任务开始前能感知并主动提示处理。
- 仅在 `approve` 后才生成正式 Skill，并自动安装到全局目录。
- `reject` 不会安装任何新 Skill，且会删除对应 pending 提案。

## 风险与兜底

- 若启动入口未执行“前置读取”，可能出现未及时提示：以 `pending/state.json` 与 `pending/index.json` 作为唯一真实来源兜底。
- 自动安装可能因权限失败：审批脚本需返回明确错误并保留已生成 Skill，便于重试安装。
- 候选名称冲突：审批阶段做名称检测，冲突时要求改名后再生成。
