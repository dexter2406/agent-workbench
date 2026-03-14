"""Filesystem install, verify, and pull logic for personal agent-workbench usage."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from agent_workbench.manifest import AgentAssetsManifest, SkillConfig


PROJECT_SKILL_ROOTS = {
    "codex": [Path(".agents") / "skills"],
    "claude": [Path(".claude") / "skills"],
    "gemini": [Path(".gemini") / "skills"],
}
GLOBAL_SKILL_ROOTS = {
    "codex": ".codex/skills",
    "claude": ".claude/skills",
    "gemini": ".gemini/skills",
}
GITIGNORE_BLOCK = [
    "# agent-workbench",
    ".agent-workbench/",
    ".agents/",
    ".claude/",
    ".codex/",
    ".gemini/",
]
SHARED_ASSETS = [
    (Path("core") / "docs" / "wt-pm-workflow.md", Path(".agents") / "docs" / "wt-pm-workflow.md"),
    (Path("core") / "rules" / "api-contract.md", Path(".claude") / "rules" / "api-contract.md"),
    (Path("core") / "rules" / "collaboration-boundaries.md", Path(".claude") / "rules" / "collaboration-boundaries.md"),
    (Path("core") / "rules" / "dod-and-safety.md", Path(".claude") / "rules" / "dod-and-safety.md"),
    (Path("core") / "rules" / "planning-with-files.md", Path(".claude") / "rules" / "planning-with-files.md"),
    (Path("core") / "plans" / "workplans" / "README.md", Path("plans") / "workplans" / "README.md"),
]
SHARED_SCRIPTS = [
    Path("plan_tracker.py"),
    Path("sync_worktree_config.ps1"),
    Path("sync_worktree_config.sh"),
]


@dataclass
class VerifyResult:
    """A single smoke-check result emitted by `bootstrap verify`."""

    status: str
    name: str
    detail: str = ""

    def render(self) -> str:
        """Return a human-readable verification line."""
        suffix = f" {self.detail}" if self.detail else ""
        return f"{self.status} {self.name}{suffix}"


def apply_manifest(target: Path, manifest: AgentAssetsManifest) -> list[str]:
    """Install project and global assets for a business repository."""
    actions: list[str] = []
    target.mkdir(parents=True, exist_ok=True)
    _ensure_gitignore(target)
    actions.append("updated .gitignore")

    _install_shared_assets(target, manifest)
    actions.extend(f"synced {destination.as_posix()}" for _, destination in SHARED_ASSETS)

    _install_shared_scripts(target, manifest)
    actions.extend(f"synced scripts/{script.name}" for script in SHARED_SCRIPTS)

    for skill in manifest.skills:
        destinations = _destinations_for_skill(skill, manifest, target, _home_dir())
        source = _source_skill_path(manifest, skill)
        for destination in destinations:
            _install_path(source, destination, mode=skill.mode)
            actions.append(f"installed {skill.scope}:{destination}")
    return actions


def pull_manifest(target: Path, manifest: AgentAssetsManifest) -> list[str]:
    """Refresh installed assets from the source repository."""
    return apply_manifest(target, manifest)


def verify_manifest(target: Path, manifest: AgentAssetsManifest) -> list[VerifyResult]:
    """Run bootstrap smoke checks and collect PASS/FAIL/SKIP results."""
    results: list[VerifyResult] = []
    home = _home_dir()

    if "project_skills" in manifest.verify:
        for skill in manifest.skills:
            if skill.scope != "project":
                continue
            for agent, roots in PROJECT_SKILL_ROOTS.items():
                if agent not in manifest.agents:
                    continue
                for root in roots:
                    destination = target / root / skill.name
                    results.append(VerifyResult(status="PASS" if destination.exists() else "FAIL", name=f"project_skill:{agent}:{skill.name}"))

    if "global_skills" in manifest.verify:
        for skill in manifest.skills:
            if skill.scope != "global":
                continue
            for agent in manifest.agents:
                destination = home / GLOBAL_SKILL_ROOTS[agent] / skill.name
                results.append(VerifyResult(status="PASS" if destination.exists() else "FAIL", name=f"global_skill:{agent}:{skill.name}"))

    if "shared_assets" in manifest.verify:
        for _, destination in SHARED_ASSETS:
            resolved = target / destination
            results.append(
                VerifyResult(
                    status="PASS" if resolved.exists() else "FAIL",
                    name=f"shared_asset:{destination.as_posix()}",
                )
            )

    if "plan_tracker" in manifest.verify:
        tracker = target / "scripts" / "plan_tracker.py"
        if tracker.exists():
            command = [sys.executable, str(tracker), "list"]
            completed = subprocess.run(command, cwd=str(target.resolve()), capture_output=True, text=True, check=False)
            results.append(VerifyResult(status="PASS" if completed.returncode == 0 else "FAIL", name="plan_tracker:list", detail=completed.stdout.strip() or completed.stderr.strip()))
        else:
            results.append(VerifyResult(status="FAIL", name="plan_tracker:list", detail="missing scripts/plan_tracker.py"))

    return results


def _install_shared_scripts(target: Path, manifest: AgentAssetsManifest) -> None:
    """Sync shared tool scripts into the business repository."""
    for script in SHARED_SCRIPTS:
        source = manifest.source_repo / "core" / "scripts" / script
        destination = target / "scripts" / script
        if source.exists():
            _install_path(source, destination, mode="link")


def _install_shared_assets(target: Path, manifest: AgentAssetsManifest) -> None:
    """Sync shared workflow docs and rules into the business repository."""
    for source_relative, destination_relative in SHARED_ASSETS:
        source = manifest.source_repo / source_relative
        if not source.exists():
            continue
        destination = target / destination_relative
        _install_path(source, destination, mode="link")


def _ensure_gitignore(target: Path) -> None:
    """Ensure the business repository ignores personal agent-workbench artifacts."""
    gitignore = target / ".gitignore"
    existing = gitignore.read_text(encoding="utf-8") if gitignore.exists() else ""
    lines = existing.splitlines()
    updated = False
    for entry in GITIGNORE_BLOCK:
        if entry not in lines:
            lines.append(entry)
            updated = True
    if updated or not gitignore.exists():
        gitignore.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


def _destinations_for_skill(skill: SkillConfig, manifest: AgentAssetsManifest, target: Path, home: Path) -> list[Path]:
    """Return all install destinations for a skill based on scope and agents."""
    destinations: list[Path] = []
    if skill.scope == "project":
        for agent in manifest.agents:
            for root in PROJECT_SKILL_ROOTS[agent]:
                destinations.append(target / root / skill.name)
    else:
        for agent in manifest.agents:
            destinations.append(home / GLOBAL_SKILL_ROOTS[agent] / skill.name)
    return destinations


def _source_skill_path(manifest: AgentAssetsManifest, skill: SkillConfig) -> Path:
    """Resolve the canonical source-repo location for a first-party skill."""
    path = manifest.source_repo / "skills" / "first_party" / skill.name
    if not path.exists():
        raise ValueError(f"Missing skill in source_repo: {path}")
    return path


def _install_path(source: Path, destination: Path, mode: str) -> None:
    """Install a file or directory using sync or best-effort link mode."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() or destination.is_symlink():
        if destination.is_dir() and not destination.is_symlink():
            shutil.rmtree(destination)
        else:
            destination.unlink()
    if mode == "link":
        try:
            os.symlink(source, destination, target_is_directory=source.is_dir())
            return
        except OSError:
            pass
    _copy_tree(source, destination)


def _copy_tree(source: Path, destination: Path) -> None:
    """Copy a file or directory tree, replacing the previous destination."""
    if destination.exists() or destination.is_symlink():
        if destination.is_dir() and not destination.is_symlink():
            shutil.rmtree(destination)
        else:
            destination.unlink()
    if source.is_dir():
        shutil.copytree(source, destination)
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def _home_dir() -> Path:
    """Resolve the per-user global install root, allowing test overrides."""
    override = os.environ.get("AGENT_ASSETS_HOME")
    return Path(override).expanduser() if override else Path.home()
