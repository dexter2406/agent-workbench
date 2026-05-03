#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
PLUGINS_MD="$REPO_ROOT/registry/plugins.md"
CLAUDE_SETTINGS="$HOME/.claude/settings.json"
CLAUDE_INSTALLED_PLUGINS="$HOME/.claude/plugins/installed_plugins.json"
CODEX_CONFIG="$HOME/.codex/config.toml"

python - "$PLUGINS_MD" "$CLAUDE_SETTINGS" "$CLAUDE_INSTALLED_PLUGINS" "$CODEX_CONFIG" <<'PY'
import json
import sys
from pathlib import Path

plugins_md, claude_settings, claude_plugins, codex_config = sys.argv[1:]

def load_json(path):
    p = Path(path)
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding="utf-8-sig"))

settings_state = load_json(claude_settings)
plugins_state = load_json(claude_plugins)
codex_text = Path(codex_config).read_text(encoding="utf-8") if Path(codex_config).exists() else ""

def plugin_installed(name, host):
    if host == "Claude plugin":
        enabled = bool((settings_state.get("enabledPlugins") or {}).get(name))
        installed = name in (plugins_state.get("plugins") or {})
        return enabled and installed
    if host == "Codex MCP server":
        return name in codex_text
    return False

def update_table(path):
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    out = []
    status_index = None
    for line in lines:
        if line.startswith("|"):
            parts = line.split("|")
            if status_index is None:
                try:
                    status_index = parts.index(" 状态 ")
                except ValueError:
                    status_index = None
            if len(parts) >= 6 and parts[1].strip() not in {"Plugin", "--------"}:
                name = parts[1].strip()
                host = parts[2].strip()
                if status_index is not None:
                    parts[status_index] = " ✅ 已装 " if plugin_installed(name, host) else " ⬜ 未装 "
                    line = "|".join(parts)
        out.append(line)
    Path(path).write_text("\n".join(out) + "\n", encoding="utf-8")

update_table(plugins_md)
PY

echo "Registry 状态已刷新："
echo "  - $PLUGINS_MD"
