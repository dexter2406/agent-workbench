#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import shutil
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent.parent
REGISTRY_MD = REPO_ROOT / "registry" / "third-party-skills.md"
REGISTRY_LOCK = REPO_ROOT / "registry" / "skills.lock.json"


@dataclass
class ReviewSummary:
    source: str
    source_url: str | None
    upstream_path: str
    key_files: list[str]
    has_scripts: bool
    risk_notes: list[str]
    recommendation: str
    skill_sha256: str | None


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_package(package: str) -> dict[str, str]:
    if "@" not in package or "/" not in package:
        raise ValueError(f"Unsupported package format: {package}")
    owner_repo, skill = package.split("@", 1)
    owner, repo = owner_repo.split("/", 1)
    return {"owner": owner, "repo": repo, "skill": skill}


def load_json_or_default(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def normalize_path_for_registry(path: Path | str) -> str:
    return str(path).replace("\\", "/")


def host_label(host: str) -> str:
    return {
        "codex-user": "installed in ~/.codex/skills",
        "claude-user": "installed in ~/.claude/skills",
        ".agents": "installed in ~/.agents/skills",
        "vendored": "vendored in this repo",
    }.get(host, host)


def notes_for_entry(host: str, local_path: str) -> str:
    normalized = normalize_path_for_registry(local_path)
    if host == "vendored":
        return f"已收录到 `{normalized}/`；上游元数据见 `registry/skills.lock.json`"
    return f"已安装到 `{normalized}`；上游元数据见 `registry/skills.lock.json`"


def detect_host_for_path(path: Path) -> str:
    home = Path.home()
    candidates = {
        "codex-user": home / ".codex" / "skills",
        "claude-user": home / ".claude" / "skills",
        ".agents": home / ".agents" / "skills",
    }
    for host, root in candidates.items():
        try:
            path.relative_to(root)
            return host
        except ValueError:
            continue
    return "vendored"


def resolve_installed_skill_path(skill_name: str) -> Path | None:
    home = Path.home()
    candidates = [
        home / ".codex" / "skills" / skill_name,
        home / ".claude" / "skills" / skill_name,
        home / ".agents" / "skills" / skill_name,
        REPO_ROOT / ".claude" / "skills" / skill_name,
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()
    return None


def directory_snapshot(path: Path) -> dict[str, Any]:
    files: list[str] = []
    hash_digest = hashlib.sha256()
    skill_md_hash = None
    for file_path in sorted(p for p in path.rglob("*") if p.is_file()):
        rel = normalize_path_for_registry(file_path.relative_to(path))
        files.append(rel)
        hash_digest.update(rel.encode("utf-8"))
        file_bytes = file_path.read_bytes()
        hash_digest.update(hashlib.sha256(file_bytes).hexdigest().encode("ascii"))
        if rel == "SKILL.md":
            skill_md_hash = hashlib.sha256(file_bytes).hexdigest()
    return {"files": files, "skill_md_hash": skill_md_hash, "directory_hash": hash_digest.hexdigest()}


def github_api_json(url: str) -> Any:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "agent-workbench/import-third-party-skill",
        },
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def github_fetch_review(package: str, source_url: str | None) -> ReviewSummary:
    pkg = parse_package(package)
    owner = pkg["owner"]
    repo = pkg["repo"]
    skill = pkg["skill"]
    source = f"{owner}/{repo}"
    source_url = source_url or f"https://github.com/{source}"
    upstream_path = f"skills/{skill}"
    base_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{urllib.parse.quote(upstream_path)}"

    try:
        top_level = github_api_json(base_url)
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"Failed to inspect upstream skill {package}: HTTP {exc.code}") from exc

    if not isinstance(top_level, list):
        raise RuntimeError(f"Unexpected GitHub response while inspecting {package}")

    top_names = sorted(item["name"] for item in top_level)
    skill_md_entry = next((item for item in top_level if item["name"] == "SKILL.md"), None)
    if not skill_md_entry:
        raise RuntimeError(f"Upstream skill {package} does not contain SKILL.md at {upstream_path}")

    skill_blob = github_api_json(skill_md_entry["url"])
    skill_bytes = base64.b64decode(skill_blob["content"])
    skill_sha256 = hashlib.sha256(skill_bytes).hexdigest()

    subdir_summaries: list[str] = []
    risk_notes: list[str] = []
    has_scripts = False
    for dirname in ("scripts", "references", "assets"):
        subdir = next((item for item in top_level if item["name"] == dirname and item["type"] == "dir"), None)
        if not subdir:
            continue
        children = github_api_json(subdir["url"])
        child_names = sorted(child["name"] for child in children if isinstance(child, dict) and "name" in child)
        preview = ", ".join(child_names[:5])
        suffix = "..." if len(child_names) > 5 else ""
        subdir_summaries.append(f"{dirname}/ ({len(child_names)}): {preview}{suffix}".rstrip())
        if dirname == "scripts":
            has_scripts = True
            risk_notes.append("Contains scripts; inspect automation before installing.")
        if dirname == "assets":
            risk_notes.append("Contains bundled assets; verify they are necessary.")

    if not risk_notes:
        risk_notes.append("No bundled scripts detected in top-level review.")

    recommendation = "Proceed after quick review."
    if has_scripts:
        recommendation = "Review scripts carefully before approving install."

    key_files = ["SKILL.md"]
    key_files.extend(name for name in top_names if name != "SKILL.md")
    key_files.extend(subdir_summaries)

    return ReviewSummary(
        source=source,
        source_url=source_url,
        upstream_path=upstream_path,
        key_files=key_files,
        has_scripts=has_scripts,
        risk_notes=risk_notes,
        recommendation=recommendation,
        skill_sha256=skill_sha256,
    )


def render_review(summary: ReviewSummary, package: str) -> str:
    lines = [
        "Upstream review:",
        f"  - Package: {package}",
        f"  - Source: {summary.source}",
        f"  - Source URL: {summary.source_url or 'n/a'}",
        f"  - Upstream path: {summary.upstream_path}",
        f"  - Has scripts: {'yes' if summary.has_scripts else 'no'}",
        "  - Key files:",
    ]
    lines.extend(f"    - {item}" for item in summary.key_files)
    lines.append("  - Risk notes:")
    lines.extend(f"    - {item}" for item in summary.risk_notes)
    lines.append(f"  - Recommendation: {summary.recommendation}")
    return "\n".join(lines)


def run_install_command(base_command: str, package: str) -> None:
    command = f"{base_command} {package} -g -y"
    result = subprocess.run(command, shell=True, cwd=REPO_ROOT)
    if result.returncode != 0:
        raise RuntimeError(f"Install command failed: {command}")


def read_registry() -> dict[str, Any]:
    return load_json_or_default(
        REGISTRY_LOCK,
        {
            "version": 1,
            "description": "Machine-readable metadata for third-party skills managed by this repository.",
            "skills": [],
        },
    )


def update_registry_lock(entry: dict[str, Any]) -> None:
    state = read_registry()
    skills = state.setdefault("skills", [])
    existing = next((item for item in skills if item.get("name") == entry["name"]), None)
    if existing:
        existing.update(entry)
    else:
        skills.append(entry)
    write_json(REGISTRY_LOCK, state)


def update_registry_markdown(name: str, host: str, source: str, local_path: str, status: str) -> None:
    row = f"| {name} | {host_label(host)} | `{source}` | {status} | {notes_for_entry(host, local_path)} |"
    lines = REGISTRY_MD.read_text(encoding="utf-8-sig").splitlines()
    updated = False
    result: list[str] = []
    for line in lines:
        if line.startswith(f"| {name} |"):
            result.append(row)
            updated = True
        else:
            result.append(line)
    if not updated:
        inserted = False
        output: list[str] = []
        for line in result:
            output.append(line)
            if not inserted and line == "|-------|------|------|------|------|":
                output.append(row)
                inserted = True
        result = output
    REGISTRY_MD.write_text("\n".join(result) + "\n", encoding="utf-8")


def compare_with_existing(
    skill_name: str,
    package: str,
    review: ReviewSummary | None,
    target_path: Path | None,
    include_installed: bool = True,
) -> str | None:
    existing_path = resolve_installed_skill_path(skill_name) if include_installed else None
    if target_path and target_path.exists():
        existing_path = target_path.resolve()
    if not existing_path:
        return None

    snapshot = directory_snapshot(existing_path)
    state = read_registry()
    lock_entry = next((item for item in state.get("skills", []) if item.get("name") == skill_name), None)
    existing_source = lock_entry.get("source") if lock_entry else "unknown"
    package_source = package.split("@", 1)[0]
    source_relation = "same source" if existing_source == package_source else "different source"
    content_relation = "unknown"
    if review and review.skill_sha256 and snapshot["skill_md_hash"]:
        content_relation = "same content" if review.skill_sha256 == snapshot["skill_md_hash"] else "different content"

    lines = [
        "Conflict detected. Installation skipped.",
        f"  - Skill: {skill_name}",
        f"  - Existing path: {existing_path}",
        f"  - Existing source: {existing_source}",
        f"  - Candidate package: {package}",
        f"  - Source relation: {source_relation}",
        f"  - Content relation: {content_relation}",
        f"  - Directory hash: {snapshot['directory_hash']}",
        "  - Key files:",
    ]
    for item in snapshot["files"][:10]:
        lines.append(f"    - {item}")
    if len(snapshot["files"]) > 10:
        lines.append(f"    - ... ({len(snapshot['files']) - 10} more)")
    lines.append("  - Decision needed: keep existing, remove it, or vendor/update explicitly.")
    return "\n".join(lines)


def status_for_entry(entry: dict[str, Any]) -> str:
    local_path = entry.get("localPath")
    host = entry.get("host")
    if not local_path:
        return "⬜ 未装"
    path = Path(local_path)
    if not path.is_absolute():
        path = REPO_ROOT / local_path
    if path.exists():
        return "✅ 已装"
    if host == ".agents":
        agents_lock = Path.home() / ".agents" / ".skill-lock.json"
        if agents_lock.exists():
            state = json.loads(agents_lock.read_text(encoding="utf-8-sig"))
            if entry["name"] in (state.get("skills") or {}):
                return "✅ 已装"
    return "⬜ 未装"


def install_mode(args: argparse.Namespace, review: ReviewSummary | None) -> int:
    conflict = compare_with_existing(args.skill_name, args.package, review, None, True)
    if conflict:
        print(conflict)
        return 0

    run_install_command(args.install_command, args.package)
    installed_path = resolve_installed_skill_path(args.skill_name)
    if not installed_path:
        raise RuntimeError(f"Installed skill '{args.skill_name}' not found after installation.")

    host = detect_host_for_path(installed_path)
    source = args.package.split("@", 1)[0]
    entry = {
        "name": args.skill_name,
        "host": host,
        "source": source,
        "sourceType": args.source_type,
        "sourceUrl": args.source_url or (review.source_url if review else None),
        "upstreamPath": review.upstream_path if review else f"skills/{args.skill_name}",
        "localPath": str(installed_path),
        "installMethod": "user-level install",
        "installCommand": f"{args.install_command} {args.package} -g -y",
        "updateCommand": f"{args.install_command} {args.package} -g -y",
        "configSource": "registry/skills.lock.json",
        "status": "installed",
        "installedAt": utc_now_iso(),
        "lastUpdatedAt": utc_now_iso(),
        "managedBy": "registry/skills.lock.json",
        "notes": "Installed to a user-managed skills directory without vendoring into this repository.",
    }
    update_registry_lock(entry)
    update_registry_markdown(args.skill_name, host, source, entry["localPath"], status_for_entry(entry))
    print("Imported third-party skill:")
    print(f"  - Name: {args.skill_name}")
    print(f"  - Host: {host_label(host)}")
    print(f"  - Installed path: {installed_path}")
    return 0


def vendor_mode(args: argparse.Namespace, review: ReviewSummary | None) -> int:
    target_dir = args.target_dir or "skills"
    target_path = (REPO_ROOT / target_dir / args.skill_name).resolve()
    conflict = compare_with_existing(args.skill_name, args.package, review, target_path, False)
    if target_path.exists() and not args.force:
        if conflict:
            print(conflict)
            return 0
        raise RuntimeError(f"Target path already exists: {target_path}")

    installed_path = resolve_installed_skill_path(args.skill_name)
    if not installed_path:
        run_install_command(args.install_command, args.package)
        installed_path = resolve_installed_skill_path(args.skill_name)
    if not installed_path:
        raise RuntimeError(f"Installed skill '{args.skill_name}' not found for vendoring.")

    if target_path.exists() and args.force:
        shutil.rmtree(target_path)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(installed_path, target_path)

    source = args.package.split("@", 1)[0]
    relative_target = normalize_path_for_registry(target_path.relative_to(REPO_ROOT))
    entry = {
        "name": args.skill_name,
        "host": "vendored",
        "source": source,
        "sourceType": args.source_type,
        "sourceUrl": args.source_url or (review.source_url if review else None),
        "upstreamPath": review.upstream_path if review else f"skills/{args.skill_name}",
        "localPath": relative_target,
        "installMethod": "vendored into this repository",
        "installCommand": f"{args.install_command} {args.package} -g -y",
        "updateCommand": f"{args.install_command} {args.package} -g -y",
        "configSource": "registry/skills.lock.json",
        "status": "installed",
        "installedAt": utc_now_iso(),
        "lastUpdatedAt": utc_now_iso(),
        "managedBy": "registry/skills.lock.json",
        "notes": "Vendored into this repository after user-approved review.",
    }
    update_registry_lock(entry)
    update_registry_markdown(args.skill_name, "vendored", source, relative_target, status_for_entry(entry))
    print("Vendored third-party skill:")
    print(f"  - Name: {args.skill_name}")
    print(f"  - Source: {installed_path}")
    print(f"  - Target: {target_path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill-name", required=True)
    parser.add_argument("--package", required=True)
    parser.add_argument("--mode", choices=["install", "vendor"], default="install")
    parser.add_argument("--target-dir", default="skills")
    parser.add_argument("--source-type", default="github")
    parser.add_argument("--source-url")
    parser.add_argument("--install-command", default="npx skills add")
    parser.add_argument("--approve", action="store_true")
    parser.add_argument("--skip-review", action="store_true")
    parser.add_argument("--force", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    review = None
    if not args.skip_review and args.source_type == "github":
        review = github_fetch_review(args.package, args.source_url)
        print(render_review(review, args.package))
        if not args.approve:
            print("Review only. Re-run with --approve to continue.")
            return 0

    if args.mode == "install":
        return install_mode(args, review)
    return vendor_mode(args, review)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
