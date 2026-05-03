# 安装器规范

`install.sh` 和 `install.ps1` 负责把 workbench 能力暴露给已选 agent 宿主。当前支持宿主：

- `claude`
- `codex`
- `gemini`

## 调用方式

默认安装到当前目录，并自动发现本机存在的已知宿主：

```bash
bash /path/to/agent-workbench/install.sh
```

```powershell
powershell -ExecutionPolicy Bypass -File D:\path\to\agent-workbench\install.ps1
```

也可以显式指定目标项目和宿主：

```bash
bash /path/to/agent-workbench/install.sh /path/to/project claude codex gemini
```

```powershell
powershell -ExecutionPolicy Bypass -File D:\path\to\agent-workbench\install.ps1 D:\path\to\project claude codex gemini
```

## 安装内容

| 来源 | 目标 | 机制 |
|------|------|------|
| `skills/` | `<host-root>/skills/` | Windows junction；Bash/Unix symlink |
| `agents/*/` | `<host-root>/agents/<name>/` | Windows junction；Bash/Unix symlink |
| `commands/*` | `<host-root>/commands/<name>` | 复制文件 |

宿主根目录：

- `claude` -> `~/.claude`
- `codex` -> `~/.codex`
- `gemini` -> `~/.gemini`

## 冲突策略

安装器是非破坏性的：

- 目标不存在：创建链接或复制文件。
- 目标已经指向当前 workbench：跳过并报告 `already linked` 或 `already copied`。
- 目标存在但内容或目标不同：跳过并报告 `conflict`。
- 不删除、不覆盖已有目录、文件或其他链接。

`commands/` 使用复制，因此 command 内容变更后需要重跑安装器同步。

## `.gitignore` 处理

安装器会确保目标项目 `.gitignore` 包含：

```gitignore
.claude/settings.local.json
```

该文件是 Claude 的本机权限状态，不应提交到项目仓库。

## 维护要求

新增宿主时必须同步更新：

- `install.sh`
- `install.ps1`
- `tests/install.ps1`
- `README.md`

安装器行为变化时，同步更新本文档。
