# Audit Agent Setup 规范

`audit-agent-setup` 由两部分组成，职责不同但协同工作：

| 位置 | 类型 | 作用 |
|------|------|------|
| `skills/audit-agent-setup/` | Skill | 审查知识库，提供规则、示例和判断基线 |
| `agents/audit-agent-setup/` | Subagent | 审查执行者，负责扫描环境、分析问题并输出报告 |

设计目标：

- 名称表达动作和对象，而不是只表达“audit”这个动作
- 内容不绑定单一宿主，适用于 Codex、Claude、Gemini 等 agent 环境
- instruction files、agent/skill/command 定义、跨宿主冲突都在审查范围内

---

## 一、Skill 部分

### 目录结构

```text
skills/audit-agent-setup/
├── SKILL.md
├── rules/
│   ├── official.md
│   └── custom.md
└── examples/
    ├── good-agent-instructions.md
    └── bad-agent-instructions.md
```

### 职责

- 提供多 agent 通用的 instruction 审查标准
- 区分通用规则与厂商特定规则
- 提供正反例，帮助 reviewer 解释“为什么好”与“为什么差”

### `SKILL.md` 要点

- `name` 为 `audit-agent-setup`
- 描述中明确动作是“审查 agent setup”
- 范围覆盖 `AGENTS.md`、`CLAUDE.md`、`GEMINI.md`、agent/skill/command 定义，以及 agentic coding 最佳实践

### `rules/official.md` 要点

- 先定义可跨宿主复用的审查原则
- 再按厂商列出应优先查阅的官方资料
- 如果某条规则只适用于某一宿主，必须显式标注

### `rules/custom.md` 要点

- 沉淀个人经验规则，不与官方规则混写
- 优先记录高频、可复用、可解释的判断标准

### `examples/` 要点

- 文件名不再绑定 `CLAUDE.md`
- 示例内容强调结构、可执行性、验证、边界与安全
- 可包含宿主注记，但不能让宿主品牌喧宾夺主

---

## 二、Subagent 部分

### 目录结构

```text
agents/audit-agent-setup/
└── agent.md
```

### 职责

- 加载 `audit-agent-setup` skill 的规则和示例
- 扫描项目级与全局级 agent setup
- 输出审查报告，不自动修改文件

### `agent.md` 要点

- `name` 为 `audit-agent-setup`
- 描述中明确支持 Codex、Claude、Gemini 等宿主
- 触发词覆盖 `/audit`、`audit agent setup`、`review AGENTS.md` 等常见表达
- 通过相对路径加载知识库，避免把 include 写死到 `~/.claude`

### 审查范围

- instruction files：`AGENTS.md`、`CLAUDE.md`、`GEMINI.md`
- 项目级 registry：`.claude/`、`.codex/`、`.gemini/` 下的 agents / skills / commands
- 全局宿主环境：宿主级 instruction、skills、agents、commands
- 冲突与缺失：同名覆盖、跨宿主矛盾、某宿主完全缺失必要 setup

### 报告要求

- 不只报告“有没有”，而是判断“好不好、为什么、怎么改”
- 引用规则时标明 `official` 或 `custom`
- 给出可直接落地的改写建议
- 保留批评力度，不做空泛鼓励

---

## 三、Command 部分

### `commands/audit.md`

保持命令名 `audit` 不变，文案改为指向 `audit-agent-setup` subagent。

这样可以保持用户入口稳定，同时完成底层命名统一。

---

## 四、兼容性与边界

- 本次改造不引入旧名别名；目标是仓库内命名统一
- 安装器与宿主可见内容若仍依赖旧安装副本，需要通过重装或重新同步获得新名称
- 仓库安装器已支持 `claude`、`codex`、`gemini` 三类宿主，审查层也保持同等覆盖
