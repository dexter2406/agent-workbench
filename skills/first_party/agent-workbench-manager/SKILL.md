---
name: agent-workbench-manager
description: Personal-use bootstrap manager for agent-workbench. Interprets natural language requests to install, verify, pull, or push first-party agent assets from the tool repo into a target business repository.
user-invokable: true
---

# agent-workbench-manager

Use this skill from inside your cloned `agent-workbench` repository after the target business repository has an `agent_assets.yaml`.

## Purpose

This skill is the natural-language entrypoint for personal `agent-workbench` management. It wraps the underlying bootstrap CLI so the user does not need to remember `apply`, `verify`, `pull`, or `push` commands.

`agent-workbench` is the control plane. The business repository is a target, not the place where management starts.

## Preconditions

Before running any command, confirm all of the following:
- The target business repository path is known.
- `agent_assets.yaml` exists in the target repository.
- If relying on manifest metadata, `source_repo` exists and is a local filesystem path.
- `skills` is non-empty.

If any precondition fails, stop and tell the user exactly what is missing.

## Trigger Phrases

Examples of user intent this skill should handle:
- `加载这个项目的 agent assets`
- `给这个项目装上 codex 和 claude skills`
- `检查这个项目的 agent-workbench 是否可用`
- `验证 Claude skills 和 plan_tracker`
- `从工具库同步这个项目的最新 assets`
- `刷新这个项目里的 skills`
- `把 wt-dev 的改动同步回工具库`
- `回推 planning-with-files 的修改`

## Action Mapping

Map user intent to exactly one CLI action:
- install / load / setup / initialize => `bootstrap apply --target-repo <path>`
- verify / check / smoke / validate => `bootstrap verify --target-repo <path>`
- update from tool repo / sync latest / refresh => `bootstrap pull --target-repo <path>`
- send changes back / promote my skill edits / sync back => `bootstrap push --target-repo <path> --skill <name>`

If the request mixes install and verify, run `apply` first and then `verify` automatically.

Unless the user explicitly overrides it, the active `agent-workbench` checkout is the source repo used for sync and push-back.

## Config Defaults

Unless a skill entry says otherwise:
- `scope` defaults to `project`
- `mode` defaults to `sync`

`task_prefix` is optional and may be omitted when the project does not use task-tracker conventions.

## Install Targets

- Project-level skills always install into `.agents/skills/`
- If `claude` is enabled, project-level skills are also mirrored into `.claude/skills/`
- Global skills install into user-level directories such as `~/.claude/skills/`

## Push Rules

- Do not read or require a `pushable` field.
- Only push skills that the user explicitly names.
- Only push skills already declared in `agent_assets.yaml`.
- Prefer the project-scope copy when the same skill exists in both project and global locations.

## Verification Interpretation

When running `verify`, report each result as `PASS`, `FAIL`, or `SKIP`.

Minimum checks expected:
- rendered templates (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md` when configured)
- project-scope skills in repo-local paths
- global-scope skills in user-level paths
- shared workflow assets in `.agents/docs/`, `.claude/rules/`, and `plans/workplans/`
- `scripts/plan_tracker.py list`

Manual checklist to include after a successful install+verify flow:
- Confirm Claude Code can see the declared Claude skills.
- Confirm the current agent host can read the rendered entry file for this project.

## Safety Rules

- Do not clone `source_repo`; the user manages cloning manually.
- Do not rewrite `agent_assets.yaml` unless explicitly asked.
- Do not assume the business repo is the control plane; require or infer a target repo path first.
- Do not push business-code changes; `push` is for explicitly named skills only.
- If `source_repo` is missing, stop and tell the user to update the local path.
- If verify fails, do not claim installation is complete.
