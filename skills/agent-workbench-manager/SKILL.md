---
name: agent-workbench-manager
description: agent-workbench 安装与维护助手。当用户说"安装 workbench"、"重装 skills"、"验证软链接"、"workbench 怎么用"、"新项目初始化" 时触发。
user-invocable: true
---

# agent-workbench-manager

`agent-workbench` 的安装、验证与日常维护指南。

## 安装机制

workbench 通过**链接映射**安装——`install.sh` / `install.ps1` 把本仓库的 `skills/`、`agents/`、`commands/` 链接到 `~/.claude/`、`~/.codex/` 和 `~/.gemini/`，修改 workbench 文件后**立即生效**，无需重新安装。

```bash
# Linux / macOS / Git Bash
bash /path/to/agent-workbench/install.sh

# Windows（需开启开发者模式）
powershell -ExecutionPolicy Bypass -File \path\to\agent-workbench\install.ps1
```

安装结果：

| 来源 | 安装到 | 机制 |
|------|--------|------|
| `skills/*/` | `~/.claude/skills/`, `~/.codex/skills/`, `~/.gemini/skills/` | 链接（Windows 为 Junction） |
| `agents/*/` | `~/.claude/agents/`, `~/.codex/agents/`, `~/.gemini/agents/` | 链接（Windows 为 Junction） |
| `commands/*` | `~/.claude/commands/`, `~/.codex/commands/`, `~/.gemini/commands/` | 链接（Windows 为 SymbolicLink） |
| `templates/CLAUDE.md.tpl` | `<目标项目>/CLAUDE.md` | 复制（仅首次） |

## 初始化新项目

```bash
bash /path/to/agent-workbench/install.sh /path/to/new-project
```

如果目标项目没有 `CLAUDE.md`，会从模板生成一份带 TODO 标注的草稿。同时在 `.gitignore` 里追加 `.claude/settings.local.json`。

## 验证安装

```bash
ls -la ~/.claude/skills/
ls -la ~/.claude/agents/
ls -la ~/.claude/commands/
# 确认软链接指向 workbench 目录，内容可读
cat ~/.claude/skills/audit-agent-setup/SKILL.md
```

常见问题：
- 软链接存在但 Claude Code 无法识别 → 重启 Claude Code
- Windows 软链接创建失败 → 确认已开启开发者模式（设置 → 系统 → 开发者选项）

## 日常维护

- **修改 skill / agent / command**：直接编辑 workbench 里的文件，保存后自动生效
- **新增 skill / agent / command**：在对应目录下添加文件后，重跑 `install.sh` / `install.ps1` 创建新链接
- **更换机器**：在新机器上 clone workbench，重跑 `install.sh` 即可恢复全部配置

## 已安装内容速查

**Skills（`~/.claude/skills/`）：**
- `audit-agent-setup` — 多 agent 项目配置审查知识库
- `wt-pm` — WT-PM 工作流知识库（规则、脚本、模板）
- `wt-plan` — Trunk 规划阶段 skill
- `wt-dev` — Worktree 开发阶段 skill
- `planning-with-files` — 文件化 planning 工作流
- `init-project-context` — 新项目上下文初始化
- `agent-workbench-manager` — 本 skill

**Agents（`~/.claude/agents/`）：**
- `audit-agent-setup` — 多 agent 项目配置审查 subagent

**Commands（`~/.claude/commands/`）：**
- `audit` — 触发 audit-agent-setup 审查
