#Requires -Version 5.1
$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))
$PluginsRegistry = Join-Path $RepoRoot "registry\plugins.md"
$ClaudeSettings = Join-Path $env:USERPROFILE ".claude\settings.json"
$ClaudeInstalledPlugins = Join-Path $env:USERPROFILE ".claude\plugins\installed_plugins.json"
$CodexConfig = Join-Path $env:USERPROFILE ".codex\config.toml"

function Get-JsonOrNull($path) {
    if (-not (Test-Path $path)) { return $null }
    return ([System.IO.File]::ReadAllText($path, [System.Text.UTF8Encoding]::new($false, $true)).Trim([char]0xFEFF)) | ConvertFrom-Json
}

function Test-PluginInstalled($name, $pluginHost, $settingsState, $installedPluginsState, $codexText) {
    if ($pluginHost -eq "Claude plugin") {
        $enabled = $false
        $installed = $false

        if ($settingsState -and $settingsState.enabledPlugins) {
            $enabled = [bool]$settingsState.enabledPlugins.PSObject.Properties[$name]
        }

        if ($installedPluginsState -and $installedPluginsState.plugins) {
            $installed = ($null -ne $installedPluginsState.plugins.PSObject.Properties[$name])
        }

        return ($enabled -and $installed)
    }

    if ($pluginHost -eq "Codex MCP server") {
        return ($codexText -match [regex]::Escape($name))
    }

    return $false
}

function Update-MarkdownTableStatus($path, $resolver) {
    $lines = Get-Content $path
    $statusIndex = $null
    $updated = foreach ($line in $lines) {
        if ($line -match '^\|') {
            $parts = $line.Split('|')
            if (-not $statusIndex) {
                $statusIndex = [Array]::IndexOf($parts, " 状态 ")
            }
            if ($parts.Length -ge 6 -and $parts[1].Trim() -notin @("Plugin", "--------")) {
                $name = $parts[1].Trim()
                $assetHost = $parts[2].Trim()
                $status = & $resolver $name $assetHost
                if ($status -and $statusIndex -gt 0) {
                    $parts[$statusIndex] = " $status "
                    ($parts -join '|')
                    continue
                }
            }
        }
        $line
    }
    Set-Content -Path $path -Value $updated -Encoding UTF8
}

$settingsState = Get-JsonOrNull $ClaudeSettings
$installedPluginsState = Get-JsonOrNull $ClaudeInstalledPlugins
$codexText = if (Test-Path $CodexConfig) { Get-Content $CodexConfig -Raw } else { "" }

Update-MarkdownTableStatus $PluginsRegistry {
    param($name, $assetHost)
    if (Test-PluginInstalled $name $assetHost $settingsState $installedPluginsState $codexText) { return "✅ 已装" }
    return "⬜ 未装"
}

Write-Host "Registry 状态已刷新："
Write-Host "  - $PluginsRegistry"
