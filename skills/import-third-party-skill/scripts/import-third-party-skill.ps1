#Requires -Version 5.1
param(
    [Parameter(Mandatory = $true)][string]$SkillName,
    [Parameter(Mandatory = $true)][string]$Package,
    [ValidateSet("install", "vendor")][string]$Mode = "install",
    [string]$TargetDir = "skills",
    [string]$SourceType = "github",
    [string]$SourceUrl,
    [string]$InstallCommand = "npx skills add",
    [switch]$Approve,
    [switch]$SkipReview,
    [switch]$Force
)

$ErrorActionPreference = "Stop"
$ScriptPath = Join-Path $PSScriptRoot "import-third-party-skill.py"

$argsList = @(
    $ScriptPath,
    "--skill-name", $SkillName,
    "--package", $Package,
    "--mode", $Mode,
    "--target-dir", $TargetDir,
    "--source-type", $SourceType,
    "--install-command", $InstallCommand
)

if ($SourceUrl) { $argsList += @("--source-url", $SourceUrl) }
if ($Approve) { $argsList += "--approve" }
if ($SkipReview) { $argsList += "--skip-review" }
if ($Force) { $argsList += "--force" }

& python @argsList
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
