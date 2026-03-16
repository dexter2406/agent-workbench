# Skills 规范

## 基本结构

每个 skill 是 `skills/` 下的一个目录，最简结构：

```
skills/
└── my-skill/
    └── SKILL.md          ← 必须，且必须是这个文件名
```

扩展结构（按需添加）：

```
skills/
└── my-skill/
    ├── SKILL.md
    ├── scripts/           ← 该 skill 专属的可执行脚本
    │   └── do-something.sh
    └── reference.md       ← 补充参考文档（SKILL.md 里用 @ 引用）
```

---

## SKILL.md 格式

每个 SKILL.md 必须以 YAML frontmatter 开头：

```markdown
---
name: skill-name              ← 用于 /skill-name 触发，kebab-case
description: >
  一句话说清楚这个 skill 做什么，以及"何时"使用它。
  Claude 靠这段描述决定是否自动加载，要写得足够具体。
---

## 正文内容

具体的指令、流程、参考资料。
```

### description 写法要点

- 说明**触发场景**，不只是功能描述
- 包含用户可能说的关键词

❌ 差：`Helps with code quality.`

✅ 好：`审查代码质量和结构。当用户要求 code review、检查代码规范、或提交前审查时使用。`

---

## 脚本放置原则

**skill 专属脚本放在自己的 `scripts/` 目录下**，不要提取到顶层。

原因：`install.sh` 以 skill 目录为单位做软链接，skill 目录是安装的原子单元。放在 skill 内部的脚本安装后路径稳定（`~/.claude/skills/{name}/scripts/`）；放在顶层则需要 install.sh 单独处理，且 skill 与脚本之间产生跨目录依赖，安装顺序出错时静默失败。

如果你发现一个脚本"需要被多个 skill 共用"，优先检查 skill 职责划分是否合理，而不是急于提取脚本。真正需要共用的情况极少，且一旦出现，应在 install.sh 里为共用脚本单独设计安装路径，并在每个依赖它的 SKILL.md 里注明依赖关系。

---

## 安装行为

`install.sh` 执行时，`skills/` 下所有 skill 目录会被复制到 `~/.claude/skills/`（全局），在所有项目里均可使用。

自定义 skills 不安装到目标项目的 `.claude/skills/`，原因：这些是个人通用能力，不与具体项目耦合。

---

## 现有 skill 内容的迁移原则

如果当前仓库里已有 skill 相关内容（无论目录名或结构如何），迁移时：

1. 保留所有现有内容
2. 调整目录名为 kebab-case 风格
3. 如果已有类似 SKILL.md 的文件但 frontmatter 不规范，补全 frontmatter，不修改正文
4. 如果 frontmatter 里没有 `name`，根据目录名推断补全
