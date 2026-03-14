# agent-workbench

Personal agent workflow assets and bootstrap tooling for Codex, Claude, and Gemini.

## What v1 includes

- A unified first-party skill: `agent-workbench-manager`
- Personal-use bootstrap CLI with `apply`, `verify`, `pull`, and `push`
- Project-local and user-global skill installation
- Smoke verification for rendered templates, installed skills, shared docs/rules, and `plan_tracker.py`
- First-party assets that can be pulled into a business repository and pushed back to the tool repo

## Recommended workflow

1. Manually clone your personal `agent-workbench` repo to a local path.
2. Add `agent_assets.yaml` to the target business repository.
3. Open the `agent-workbench` repo when you want to sync or verify assets.
4. Use the `agent-workbench-manager` skill in natural language, for example:
   - `加载这个项目的 agent assets 并验证`
   - `从工具库同步这个项目的最新 skills`
   - `把 wt-dev 的改动回推到工具库`

The CLI remains available as the execution layer and fallback. Commands are launched from `agent-workbench`, and the business repo is passed as `--target-repo`:

```bash
python -m agent_workbench.cli apply --target-repo ../my-project
python -m agent_workbench.cli verify --target-repo ../my-project
python -m agent_workbench.cli pull --target-repo ../my-project
python -m agent_workbench.cli push --target-repo ../my-project --skill wt-dev
```

## Consumer manifest

```yaml
source_repo: ../agent-workbench
agents:
  - codex
  - claude
skills:
  - agent-workbench-manager
  - planning-with-files
  - cross-worktree-sync
  - name: wt-plan
    scope: global
templates:
  - codex
  - claude
verify:
  - templates
  - project_skills
  - global_skills
  - shared_assets
  - plan_tracker
```

Skill defaults:
- `scope`: `project`
- `mode`: `sync`

Installation behavior:
- Project-level skills are always installed to `.agents/skills/`
- If `claude` is enabled, the same project-level skills are also installed to `.claude/skills/`
- Global skills are installed to `~/.claude/skills/`, `~/.codex/skills/`, or `~/.gemini/skills/` depending on enabled agents
- Shared workflow assets are synced to `.agents/docs/`, `.claude/rules/`, and `plans/workplans/README.md`
- Shared tool scripts are synced to `scripts/plan_tracker.py`, `scripts/sync_worktree_config.ps1`, and `scripts/sync_worktree_config.sh`

Notes:
- `agent-workbench` is the control plane. `apply`, `verify`, `pull`, and `push` are intended to run from the tool repo, not from inside the business repo.
- `source_repo` stays in `agent_assets.yaml` mainly as a source-of-truth pointer for local setups and push-back discovery; CLI calls from `agent-workbench` will use the current tool repo by default.
- `task_prefix` is optional and only matters if your project wants to reuse task-tracker conventions.
- `push` no longer reads a `pushable` flag; you choose what to push by passing `--skill <name>`.
