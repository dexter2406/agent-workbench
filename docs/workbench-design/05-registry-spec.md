# Registry 规范

## 定位

`registry/` 是第三方资产的登记入口。
用途：记录你安装或 vendoring 的第三方工具，方便换机器、重装和状态校验。

## 文件格式

### `registry/third-party-skills.md`

```markdown
# Third-party Skills

| Skill | 宿主 | 来源 | 状态 | 备注 |
|-------|------|------|------|------|
| frontend-design | installed in ~/.codex/skills | `anthropics/skills` | ✅ 已装 | 已安装到 `C:/Users/name/.codex/skills/frontend-design`；上游元数据见 `registry/skills.lock.json` |
| web-design | vendored in this repo | `vercel-labs/agent-skills` | ✅ 已装 | 已收录到 `skills/web-design/`；上游元数据见 `registry/skills.lock.json` |

## 说明
- ✅ 已装：当前机器上可用
- ⬜ 未装：registry 已登记，但当前机器未检测到
- `registry/skills.lock.json` 保存机器可读元数据，含来源、宿主、路径与更新命令
```

### `registry/plugins.md`

```markdown
# Plugins / MCP

| Plugin | 安装方式 | 状态 |
|--------|----------|------|
| github-integration | `npx claude-code-templates@latest --mcp development/github-integration` | ⬜ 待装 |

## 说明
- ✅ 已装
- ⬜ 待装
- ⏸️ 暂停
```

## 生成要求

如果当前仓库里已有类似的清单文件（任何格式），将内容迁移到上述格式中，不要丢弃已有记录。
如果没有，生成上述空模板即可。

