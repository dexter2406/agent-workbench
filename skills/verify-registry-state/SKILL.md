---
name: verify-registry-state
description: 检查 registry 中登记的 plugins 是否在当前机器可用，并刷新插件状态。
user-invocable: true
---

# verify-registry-state

用于刷新 `registry/plugins.md` 中插件和 MCP 类资产的状态。

`registry/third-party-skills.md` 现在只是第三方 skills 的人工来源清单。第三方 skills 的正式内容直接放在 `skills/<name>/`，不再维护状态列，也不再依赖旧的 skills lock JSON。

## 检查范围

- `registry/plugins.md`

## 状态约定

- `✅ 已装`
- `⬜ 未装`

## 检查规则

当前支持：

- `Claude plugin`：同时检查 `~/.claude/settings.json` 中是否启用，以及 `~/.claude/plugins/installed_plugins.json` 中是否已安装
- `Codex MCP server`：检查 `~/.codex/config.toml` 中是否存在对应 server 名称

## 执行方式

Windows:

```powershell
powershell -ExecutionPolicy Bypass -File skills/verify-registry-state/scripts/verify-registry-state.ps1
```

Linux / macOS:

```bash
bash skills/verify-registry-state/scripts/verify-registry-state.sh
```

## 预期结果

- 刷新 `registry/plugins.md` 的状态列
- 不自动安装缺失项
