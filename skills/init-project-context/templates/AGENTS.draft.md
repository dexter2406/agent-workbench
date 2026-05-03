# Agent Instructions Draft

This is the canonical agent instruction file for this repository. If another host-specific entry file is needed, make it point here instead of duplicating guidance.

## Scope

- Repository purpose:
- Important repository boundaries:
- Code or directories that are reference-only:

## Documentation Index

Use these directories as a progressive-disclosure index. Open only the docs that are relevant to the current task:

- `docs/top-level-knowledge/` — stable project context, tech stack, architecture notes, references, and core logic maps.
- `docs/epic-plans/` — epic-level plans, roadmaps, milestone direction, and broad acceptance strategy.
- `docs/func-design/` — focused feature/module designs that serve an epic.
- `docs/impl-plans/` — temporary coding plans; move completed and accepted plans to `docs/impl-plans/archive/`.

Keep detailed project knowledge in docs, not in this file.

## Commands

- Install:
- Run:
- Test:
- Build:

## Rules

- Preserve user changes in the worktree.
- Keep implementation code separate from reference material.
- Run relevant verification before claiming completion.
- If no runnable verification exists for a docs-only change, say so explicitly.
- Use `exchange/` only for temporary information and do not treat it as durable knowledge.

## Open Questions

Track unresolved product and architecture questions in `docs/top-level-knowledge/`, not here.
