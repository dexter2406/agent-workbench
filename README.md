# agent-workbench

Personal agent workflow assets and bootstrap tooling for Codex, Claude, and Gemini.

## What v1 includes

- A unified first-party skill: `agent-workbench-manager`
- Personal-use bootstrap CLI with `apply`, `verify`, and `pull`
- Project-local and user-global skill installation
- Smoke verification for installed skills, shared docs/rules, and `plan_tracker.py`
- First-party assets that can be linked or synced into a business repository from the tool repo

## Recommended workflow

1. Manually clone your personal `agent-workbench` repo to a local path.
2. Optionally add `agent_assets.yaml` to the target business repository if you want to customize agents or skills.
3. Open the `agent-workbench` repo when you want to sync or verify assets.
4. Use the `agent-workbench-manager` skill in natural language, for example:
   - `加载这个项目的 agent assets 并验证`
   - `从工具库同步这个项目的最新 skills`
   - `在没有 agent_assets.yaml 的仓库里直接加载默认 assets`

The CLI remains available as the execution layer and fallback. Commands are launched from `agent-workbench`, and the business repo is passed as `--target-repo`:

```bash
python -m agent_workbench.cli apply --target-repo ../my-project
python -m agent_workbench.cli verify --target-repo ../my-project
python -m agent_workbench.cli pull --target-repo ../my-project
```

## Workflow

1. Clone `agent-workbench` to any local path, for example `D:\Tools\agent-workbench`.
2. Open the cloned `agent-workbench` repo when you want to install or refresh assets for a business repository.
3. Run `apply`, `verify`, or `pull` with the business repository path passed through `--target-repo`.
4. Edit first-party skills, shared docs, shared rules, and shared scripts in `agent-workbench`, then run `apply` or `pull` again to refresh the business repository.

## Use Cases

- Load assets into a repository that already has `agent_assets.yaml`:
  `python -m agent_workbench.cli apply --target-repo ../my-project`
- Verify installed assets in a repository with an existing manifest:
  `python -m agent_workbench.cli verify --target-repo ../my-project`
- Refresh a project after updating skills or shared scripts inside `agent-workbench`:
  `python -m agent_workbench.cli pull --target-repo ../my-project`
- Initialize a repository that has no `agent_assets.yaml` yet:
  `python -m agent_workbench.cli apply --target-repo ../my-project`
- Ask the manager skill to run the same flow in natural language:
  `加载这个项目的 agent assets 并验证`
  `从工具库同步这个项目的最新 skills`
  `在没有 agent_assets.yaml 的仓库里直接加载默认 assets`

## Installed Paths

- First-party skills are installed to `.agents/skills/`
- Claude project skills are also installed to `.claude/skills/`
- Gemini project skills are also installed to `.gemini/skills/`
- Shared workflow docs are installed to `.agents/docs/`
- Shared workflow rules are installed to `.claude/rules/`
- Shared workplan docs are installed to `plans/workplans/README.md`
- Shared scripts are installed to `scripts/plan_tracker.py`, `scripts/sync_worktree_config.ps1`, and `scripts/sync_worktree_config.sh`

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
verify:
  - project_skills
  - global_skills
  - shared_assets
  - plan_tracker
```

Skill defaults:
- `scope`: `project`
- `mode`: `link`

Installation behavior:
- Project-level skills are installed to `.agents/skills/`
- If `claude` is enabled, the same project-level skills are also installed to `.claude/skills/`
- If `gemini` is enabled, the same project-level skills are also installed to `.gemini/skills/`
- Global skills are installed to `~/.claude/skills/`, `~/.codex/skills/`, or `~/.gemini/skills/` depending on enabled agents
- Shared workflow assets are linked when possible, with copy fallback, to `.agents/docs/`, `.claude/rules/`, and `plans/workplans/README.md`
- Shared tool scripts are linked when possible, with copy fallback, to `scripts/plan_tracker.py`, `scripts/sync_worktree_config.ps1`, and `scripts/sync_worktree_config.sh`
- If `agent_assets.yaml` is missing, `apply` and `pull` load all first-party skills by default

Notes:
- `agent-workbench` is the control plane. `apply`, `verify`, and `pull` are intended to run from the tool repo, not from inside the business repo.
- `source_repo` stays in `agent_assets.yaml` mainly as a source-of-truth pointer for local setups; CLI calls from `agent-workbench` will use the current tool repo by default.
- `task_prefix` is optional and only matters if your project wants to reuse task-tracker conventions.
- Business-repo copies should be treated as generated install targets; edit the source files in `agent-workbench` instead.
