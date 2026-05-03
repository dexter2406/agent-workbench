# Audit Agent Setup 规范

`audit-agent-setup` 用于审查当前仓库或目标项目的 agent setup 质量。它由 skill 和 subagent 两部分组成：

| 位置 | 类型 | 职责 |
|------|------|------|
| `skills/audit-agent-setup/` | Skill | 提供审查规则、示例和判断基线 |
| `agents/audit-agent-setup/` | Subagent | 扫描环境、分析问题并输出报告 |

## 设计目标

- 覆盖 Codex、Claude、Gemini 等多宿主环境。
- 审查 instruction files、agent/skill/command 定义和跨宿主冲突。
- 输出可执行的改进建议，而不是只检查文件是否存在。

## Skill 部分

推荐结构：

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

要求：

- `SKILL.md` 的 `name` 为 `audit-agent-setup`。
- description 明确说明用于审查 agent setup。
- `rules/official.md` 记录官方或厂商规则；宿主特定规则必须显式标注适用宿主。
- `rules/custom.md` 沉淀个人经验规则，不和官方规则混写。
- `examples/` 使用宿主中立命名，示例聚焦结构、可执行性、验证、边界与安全。

## Subagent 部分

`agents/audit-agent-setup/agent.md` 是执行者定义。

要求：

- `name` 为 `audit-agent-setup`。
- description 覆盖 `/audit`、`audit agent setup`、`review AGENTS.md`、`review CLAUDE.md`、`review GEMINI.md` 等常见触发表达。
- 通过相对路径加载 `skills/audit-agent-setup/` 下的知识库，避免绑定到某个用户目录或单一宿主。
- 审查结束后只输出报告，不自动修改文件。

## 审查范围

项目级：

- `AGENTS.md`、`CLAUDE.md`、`GEMINI.md`
- `.claude/agents|skills|commands`
- `.codex/agents|skills|commands`
- `.gemini/agents|skills|commands`
- 其他明显的 agent 宿主目录或 instruction 入口
- `.gitignore`

全局宿主级：

- `~/.claude/`、`~/.codex/`、`~/.gemini/` 下的 instruction 文件
- 各宿主 `skills/`、`agents/`、`commands/` 清单

## 报告要求

- 判断“好不好、为什么、怎么改”，不要只报告“有/没有”。
- 引用规则时标明来源：`official` 或 `custom`。
- 对问题给出可直接落地的改写建议。
- 对同名 agent、skill、command 说明优先级和冲突影响。
- 对缺失项说明为什么值得补，而不是生成泛泛 checklist。

## Command 入口

`commands/audit.md` 保持命令名 `audit`，内容指向 `audit-agent-setup` subagent。这样用户入口稳定，底层职责保持清晰。
