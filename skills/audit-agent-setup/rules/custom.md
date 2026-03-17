# Custom Rules（个人经验积累）

这个文件存放从实践中提炼出来的判断标准。
它不是官方文档的复述，而是你在多 agent 协作里反复验证过的经验。

每次你发现某个 agent setup 特别好或特别差，都把结论收敛到这里。
这个文件会随 workbench 版本迭代，形成你自己的审查基线。

---

## Rule C1: 先写宿主无关规则，再补宿主差异

**原则**：优先把 instruction 文件写成“通用行为规则 + 宿主差异说明”的结构，而不是从一开始就绑定某个宿主的专有术语。

**来源**：同一项目往往同时给 Codex、Claude、Gemini 使用。若规则全部写死在某个宿主术语里，迁移和审查成本会快速上升。

✅ 好的写法：
```markdown
## Required verification
- Run the project test command before claiming completion.
- If a host requires a special verification wrapper, document it in a host-specific note.

## Host notes
- Codex: prefer `rg` for repo search when available.
- Claude: check project and global instructions for conflicts.
```

❌ 差的写法：
```markdown
Always follow Claude memory rules.
Use Claude subagents for every task.
If Claude says X, do X.
```

**差在哪**：前者先表达项目真正想要的行为，再补充宿主差异；后者把项目规范错误地等同于某一个工具的品牌规范。

---

## Rule C2: 指令文件要优先服务执行，不要写成宣言

**原则**：instruction 文件应该优先包含项目上下文、执行命令、验证步骤、禁区和边界，而不是口号式价值观。

**来源**：很多低质量配置写满“be helpful”“follow best practices”，但对 agent 实际没有可操作价值。

✅ 好的写法：
```markdown
## Verification
- Run `npm test`
- Run `npm run build`
- Do not claim completion unless both exit with code 0.
```

❌ 差的写法：
```markdown
Write clean code.
Be thoughtful.
Make sure everything works.
```

**差在哪**：差的写法无法转化为可执行行为，也无法在 review 中稳定判断是否满足。
