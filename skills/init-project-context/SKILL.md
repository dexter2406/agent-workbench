---
name: init-project-context
description: Use when starting a new or under-documented repository that lacks a clear project definition. Use this skill when the project purpose, deliverables, boundaries, doc taxonomy, or candidate tech direction are still vague and need to be clarified before implementation planning. Default to stabilizing project context first; only draft lightweight agent instruction files later if the user explicitly wants them.
---

# Init Project Context

## Overview

Initialize project foundation before feature planning. The goal is to turn a vague repository into one with enough project definition, scope boundaries, document structure, and technical direction to support later planning.

Common path for early-stage repositories:
`stabilize project meaning -> choose technical direction -> write docs/top-level-knowledge -> optionally create epic/function/implementation planning docs`

**REQUIRED SUB-SKILL:** Use `brainstorming` for conversational discovery.

This skill does **not** start by writing agent entry files. It first stabilizes the project itself. Agent entry files are optional follow-up outputs, not the default center of gravity.

If the user clearly intends to enter WT-PM or another task/worktree workflow next, this skill may continue past foundation docs into planning and handoff. That extension is still part of project-context initialization; it is not a replacement for `wt-plan`.

## Default Documentation Taxonomy

Use this `docs/` taxonomy by default for new or reorganized projects:

- `docs/top-level-knowledge/` — stable project knowledge: project context, technology stack, architecture notes, porting references, core logic maps.
- `docs/epic-plans/` — epic-level plans, roadmaps, milestone direction, and broad acceptance strategy.
- `docs/func-design/` — focused feature/module designs that close part of an epic.
- `docs/impl-plans/` — temporary coding plans, detailed implementation steps, sequencing, and verification notes.
- `docs/impl-plans/archive/` — completed implementation plans after implementation and acceptance.

Each of the four main `docs/` directories should have a short `README.md` that defines the directory's purpose. These README files are not file indexes and should not try to maintain a list of every document inside.

Root-level structure outside `docs/` is project-specific. The only default extra convention is `exchange/`:

- `exchange/` is for temporary information exchange, scratch notes, copied snippets, one-off research dumps, and transient handoff material.
- `exchange/` is not a long-term knowledge source.
- Add `exchange/` to `.gitignore` by default when creating it.

## Output Model

This skill works in three documentation layers, plus optional agent entry docs.

### Layer 1: Top-Level Knowledge

Create or draft these first:

- A project definition document under `docs/top-level-knowledge/`, such as `project-context.md`, `prd.md`, or an existing equivalent name.
- `docs/top-level-knowledge/tech-stack.md`

Purpose: project definition. These documents explain what the project is, why it exists, what milestone matters now, and the provisional technical direction.

For greenfield repositories, default to `project-context.md`. For existing repositories, keep a clear existing name such as `prd.md` instead of renaming it mechanically.

### Layer 2: Planning And Design Docs

Create these after Layer 1 is stable when the user needs approved direction:

- `docs/epic-plans/*` for milestone, roadmap, and epic-level direction.
- `docs/func-design/*` for feature/module design details that serve an epic.

Purpose: solution planning. These documents freeze product, design, and technical direction at the right granularity before implementation.

### Layer 3: Implementation Plans

Create these only when the user is ready to decompose approved direction into coding work:

- `docs/impl-plans/*`
- `docs/impl-plans/archive/*` for completed and accepted implementation plans.

Purpose: execution tracking. These artifacts break approved intent into task-level work with dependencies, sequencing, file-level notes, and verification commands. They are temporary by nature.

### Optional Layer 4: Agent Entry Docs

Create these only after Layer 1 is stable and only if the user explicitly wants them:

- One canonical instruction file chosen for the project's actual agent host, such as `AGENTS.md`, `CLAUDE.md`, or `GEMINI.md`.
- Any additional host-specific filenames should point to the canonical file through a symlink, hard link, or short pointer file.

Do not hardcode `AGENTS.md` as the universal canonical file. Confirm or infer the main host first. For example:

- Claude-first projects may keep the body in `CLAUDE.md` and make `AGENTS.md` point to it.
- Codex-first projects may keep the body in `AGENTS.md` and make `CLAUDE.md` point to it if needed.

Keep agent entry files lightweight: scope, documentation index, commands, rules, and critical constraints. Do not dump project details into them. Use progressive disclosure: point agents to the relevant documentation directories and let them open only the docs needed for the current task.

If the repository is still ambiguous, stop after Layer 1 and list remaining open questions. Do not create planning, implementation, or agent-entry artifacts from unresolved project definition.

## Workflow

### Phase 1: Repo Discovery

Before asking questions, inspect the repository for discoverable facts:

- top-level structure
- current `docs/` structure and existing knowledge/planning docs
- runtime manifests and lockfiles
- backend/frontend entrypoints
- test commands
- CI, scripts, schema directories, task trackers, worktree conventions
- existing agent entry files and whether they duplicate each other
- existing `.gitignore` and whether transient exchange/scratch directories are ignored

Record findings under these buckets:

- `confirmed facts`
- `reasonable inferences`
- `critical gaps`
- `conflicts`

Never ask the user for information that the repository already makes clear.

### Phase 2: Context Closure

Use guided discovery to close the highest-impact gaps.

Ask one question at a time. Each question must help determine at least one of:

- project purpose
- primary user or audience
- current milestone
- in-scope / out-of-scope
- required deliverables
- educational or business context
- candidate technical direction
- hard constraints
- preferred documentation taxonomy if the default does not fit
- canonical agent entry file, if agent files are requested

If the user answers vaguely, do not move on. Narrow the current question until it is actionable.

Use this pattern:

1. summarize what is already known
2. state what is still unclear
3. ask one high-value question

### Phase 3: Foundation Drafting

Once the repository is sufficiently defined, draft the foundation docs using the templates in `templates/`.

Use repository evidence plus user answers. Mark uncertain content explicitly instead of pretending certainty.

Create the four `docs/` directory README files when creating the taxonomy. Keep each README short and definitional.

### Phase 4: Planning And Design

Once the foundation docs are stable and the user wants implementation direction:

- create or update epic-level plans under `docs/epic-plans/`
- create or update feature/module designs under `docs/func-design/`
- use those docs to freeze product, design, and technical direction before coding

Rules:

- use `docs/epic-plans/` for broad milestone direction
- use `docs/func-design/` for narrower feature/module decisions
- do not confuse design/planning docs with temporary implementation plans
- if the design is still changing, stay here instead of preparing implementation plans

### Phase 5: Implementation Handoff

Only after the solution direction is approved and the user wants coding work decomposed:

- create or update implementation plans under `docs/impl-plans/`
- include dependencies, sequencing, task-local findings, file-level notes, and verification commands
- move completed and accepted plans to `docs/impl-plans/archive/`

If the repository uses WT-PM or another tracked execution workflow, adapt these docs to that workflow without duplicating the full WT-PM lifecycle here.

#### No-git bootstrap mode

If the repository is not yet a git repo or cannot support worktrees yet:

- it is still acceptable to prepare `docs/impl-plans/` bootstrap artifacts
- explicitly mark them as pre-WT-PM or pre-tracking bootstrap files
- do not pretend branches, trunk, or worktrees already exist
- defer formal `wt-plan` execution until git/trunk/worktree prerequisites are available

### Phase 6: Instruction Drafting

Only after foundation docs are strong enough, and after any needed planning/handoff layers are in place:

- choose one canonical agent entry file based on actual project usage
- create the canonical file with scope, documentation index, commands, rules, and constraints only
- identify which additional host-specific filenames are actually required
- prefer symlink, then hard link, then short pointer file for non-canonical names
- keep one authoritative instruction body instead of duplicating content across agents

Before creating compatibility aliases, confirm the user really uses that agent. If there is no confirmed consumer, do not create speculative aliases.

## Sufficiency Check

The project is ready for instruction drafting only if all of these are true:

- The project purpose is explicit.
- The primary users or operators are explicit.
- The current milestone or delivery horizon is explicit.
- Required deliverables are explicit.
- In-scope and out-of-scope are explicit enough for planning.
- There is at least a provisional candidate tech direction or an explicit statement that tech selection is still open.
- The documentation taxonomy is clear enough for future docs to be placed predictably.
- Future planning would not depend on repeated oral clarification of core context.

If any of these fail, continue discovery instead of drafting instruction files.

The project is ready for implementation handoff only if all of these are also true:

- The current milestone is explicit enough to plan task boundaries.
- The first task decomposition is explicit enough to create implementation plan docs.
- Dependencies and sequencing are clear enough to assign order or parallelism.
- The user actually wants tracked or written implementation planning rather than direct implementation.

If any of these fail, keep working at the foundation or planning/design layer.

## Heuristics

### Treat as Project-Specific

Usually keep in `docs/top-level-knowledge/`:

- project background and rationale
- business domain and user scenarios
- milestone status
- required deliverables
- in-scope / out-of-scope boundaries
- technical direction that is still provisional
- stable architecture or porting references

Usually keep in `docs/epic-plans/`:

- approved milestone strategy
- broad product flow
- multi-feature roadmap
- epic-level acceptance criteria

Usually keep in `docs/func-design/`:

- feature/module behavior
- component boundaries
- data flow
- error handling
- narrower acceptance criteria

Usually keep in `docs/impl-plans/`:

- task rows and task ids
- sequencing and dependencies
- file-by-file coding notes
- task-local findings and progress logs
- verification commands and status

Usually keep in agent entry files:

- scope and repository boundaries
- lightweight documentation index
- common commands
- durable rules and constraints
- host-specific compatibility notes

### Treat as Reusable Template Material

Usually fit into skill templates:

- section structures
- directory README definitions
- lightweight documentation index pattern
- canonical-agent-file selection guidance
- links back to shared context docs

## Question Areas

When discovery leaves gaps, prioritize these topics in order:

1. What is the project actually for?
2. Is it a real product, an internal tool, a prototype, or a course project?
3. What is the smallest milestone that matters right now?
4. What must be delivered?
5. What is explicitly out of scope?
6. What technical direction is currently being considered?
7. Does the default `docs/` taxonomy fit this project?
8. Does the user want epic-level planning, function/module design, or implementation planning after context stabilization?
9. Does the user intend to enter WT-PM or another tracked execution workflow next?
10. Which agent entry filename should be canonical, if any?

## Drafting Rules

- Prefer concise, operational language.
- Separate facts from assumptions.
- Separate project definition from technical speculation.
- Prefer templates with placeholders over fake certainty.
- Preserve future extensibility without forcing agent scaffolding too early.
- Separate top-level knowledge, epic plans, function designs, and implementation plans instead of collapsing them into one file set.
- Keep existing project-definition filenames when they are clear, such as `prd.md`; do not force-rename them to `project-context.md`.
- Use `tech-stack.md` for the default technology-stack document.
- Keep directory README files definitional; do not maintain file indexes there.
- Keep one canonical agent instruction body; point other host files to it.
- Prefer links or aliases over duplicated agent-specific instruction files.
- Use symlinks first, hard links second, short pointer files last.
- Do not create agent-specific aliases until their consumers are confirmed.
- Do not create implementation plan artifacts until approved direction is stable enough to decompose.
- Add `exchange/` to `.gitignore` if creating or relying on that temporary directory.

## Common Mistakes

| Mistake | Better Approach |
|---|---|
| Drafting agent entry files immediately | Build top-level knowledge first |
| Asking broad questions in batches | Ask one high-value question at a time |
| Treating vague goals as sufficient | Narrow them to a milestone and success condition |
| Jumping straight from context discovery to implementation plans | Freeze direction in epic/function docs first |
| Repeating repo facts back as questions | Discover locally first |
| Making agent workflow the main story | Make the project itself the main story |
| Stuffing project meaning into agent files | Keep core context in shared docs |
| Turning directory README files into manual indexes | Keep README files as concise directory definitions |
| Pretending unknowns are known | Mark open questions explicitly |
| Maintaining parallel `AGENTS.md` and `CLAUDE.md` bodies | Keep one canonical body and point other files to it |
| Assuming `AGENTS.md` must always be canonical | Choose canonical file based on actual host usage |
| Letting implementation plans drift from approved design docs | Treat epic/function docs as the higher-level source of truth unless design is intentionally revised |
| Treating `exchange/` as durable knowledge | Move lasting information into the appropriate `docs/` directory |

## Files and Templates

Use the templates in this skill directory:

- `templates/project-context.md`
- `templates/tech-stack.md`
- `templates/AGENTS.draft.md`
- `templates/docs/top-level-knowledge/README.md`
- `templates/docs/epic-plans/README.md`
- `templates/docs/func-design/README.md`
- `templates/docs/impl-plans/README.md`

Use the first two templates by default under `docs/top-level-knowledge/` for new projects. In existing projects, the project-definition template may map to `project-context.md`, `prd.md`, or another clear equivalent name. Use the directory README templates when initializing the default docs taxonomy.

Only use the agent-entry template when the user explicitly asks for agent-facing files. Rename the drafted file to the chosen canonical host file if needed, and make other requested host filenames point to it instead of duplicating content.

If the user intends to enter WT-PM or file-based execution tracking after context stabilization, point to the relevant WT-PM / `planning-with-files` conventions, but keep this skill focused on preparing repository context and handoff state.

For realistic usage patterns and conversation shape, see `usage-examples.md`.
