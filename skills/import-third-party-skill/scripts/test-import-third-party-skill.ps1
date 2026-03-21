#Requires -Version 5.1
$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))
$ImportScript = Join-Path $PSScriptRoot "import-third-party-skill.py"
$VerifyScript = Join-Path $RepoRoot "skills\verify-registry-state\scripts\verify-registry-state.ps1"
$TempRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("import-third-party-skill-tests-" + [System.Guid]::NewGuid().ToString("N"))

function Assert-True($Condition, $Message) {
    if (-not $Condition) {
        throw $Message
    }
}

try {
    New-Item -ItemType Directory -Path $TempRoot | Out-Null
    $FakeHome = Join-Path $TempRoot "home"
    New-Item -ItemType Directory -Path $FakeHome | Out-Null
    $env:USERPROFILE = $FakeHome
    $env:HOME = $FakeHome

    $RegistryMd = Join-Path $RepoRoot "registry\third-party-skills.md"
    $RegistryLock = Join-Path $RepoRoot "registry\skills.lock.json"
    $RegistryMdBackup = Get-Content $RegistryMd -Raw
    $RegistryLockBackup = Get-Content $RegistryLock -Raw

    $FakeInstaller = Join-Path $TempRoot "fake-installer.ps1"
    @'
param([string]$Package, [string]$Flag1, [string]$Flag2)
$skillName = ($Package -split "@", 2)[1]
$target = Join-Path $env:USERPROFILE ".codex\skills\$skillName"
New-Item -ItemType Directory -Path $target -Force | Out-Null
Set-Content -Path (Join-Path $target "SKILL.md") -Value "---`nname: $skillName`n---" -Encoding UTF8
Set-Content -Path (Join-Path $target "manifest.txt") -Value "fixture" -Encoding UTF8
'@ | Set-Content -Path $FakeInstaller -Encoding UTF8

    @'
# Third-party Skills

| Skill | 宿主 | 来源 | 状态 | 备注 |
|-------|------|------|------|------|

## 说明
- 机器可读元数据见 `registry/skills.lock.json`
'@ | Set-Content -Path $RegistryMd -Encoding UTF8

    @'
{
  "version": 1,
  "description": "Machine-readable metadata for third-party skills managed by this repository.",
  "skills": []
}
'@ | Set-Content -Path $RegistryLock -Encoding UTF8

    & python $ImportScript `
        --skill-name "frontend-design" `
        --package "anthropics/skills@frontend-design" `
        --skip-review `
        --approve `
        --install-command "powershell -ExecutionPolicy Bypass -File $FakeInstaller" | Out-Null

    $lockState = Get-Content $RegistryLock -Raw | ConvertFrom-Json
    $entry = $lockState.skills | Where-Object { $_.name -eq "frontend-design" } | Select-Object -First 1
    Assert-True ($null -ne $entry) "install mode should register skill"
    Assert-True ($entry.host -eq "codex-user") "install mode should use codex-user host"
    Assert-True ($entry.localPath -like "*\.codex\skills\frontend-design") "install mode should record user path"

    $mdText = Get-Content $RegistryMd -Raw
    Assert-True ($mdText -match "installed in ~/.codex/skills") "markdown registry should show codex host"

    $conflictOutput = & python $ImportScript `
        --skill-name "frontend-design" `
        --package "vercel-labs/agent-skills@frontend-design" `
        --skip-review `
        --approve `
        --install-command "powershell -ExecutionPolicy Bypass -File $FakeInstaller"

    Assert-True (($conflictOutput -join "`n") -match "Conflict detected\. Installation skipped\.") "same-name install should skip on conflict"

    & python $ImportScript `
        --skill-name "frontend-design" `
        --package "anthropics/skills@frontend-design" `
        --mode vendor `
        --skip-review `
        --approve `
        --target-dir "skills" | Out-Null

    $vendoredPath = Join-Path $RepoRoot "skills\frontend-design\SKILL.md"
    Assert-True (Test-Path $vendoredPath) "vendor mode should copy skill into repo"

    & powershell -ExecutionPolicy Bypass -File $VerifyScript | Out-Null
    $mdRefreshed = Get-Content $RegistryMd -Raw
    Assert-True ($mdRefreshed -match "vendored in this repo") "verify should preserve vendored host visibility"

    Write-Host "All import-third-party-skill tests passed."
}
finally {
    if (Test-Path (Join-Path $RepoRoot "skills\frontend-design")) {
        Remove-Item (Join-Path $RepoRoot "skills\frontend-design") -Recurse -Force
    }
    if ($RegistryMdBackup) {
        Set-Content -Path $RegistryMd -Value $RegistryMdBackup -Encoding UTF8
    }
    if ($RegistryLockBackup) {
        Set-Content -Path $RegistryLock -Value $RegistryLockBackup -Encoding UTF8
    }
    if (Test-Path $TempRoot) {
        Remove-Item $TempRoot -Recurse -Force
    }
}
