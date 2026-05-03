---
name: project-knowledge-manager
description: Use when preserving, curating, routing, summarizing, or maintaining durable project knowledge after a task, milestone, investigation, implementation, refactor, integration, debugging session, retrospective, runbook, verification note, or hands-on experience. This is the parent entrypoint for docs/hands-on-knowledge and should decide whether to use impl-knowledge-maintainer, debug-knowledge-maintainer, both, or a higher-level project documentation destination.
---

# Project Knowledge Manager

Route durable project hands-on knowledge to the right maintained home.

This skill is the parent entrypoint for `docs/hands-on-knowledge/`. It classifies incoming material, decides which maintainer skill should handle it, and keeps the project knowledge layer coherent without duplicating the detailed rules owned by the child skills.

Treat references to `docs/hadns-on-experience`, `hands-on-experience`, or similar wording as the existing `docs/hands-on-knowledge/` convention unless the repository clearly defines a different path.

## Knowledge Layer

Use `docs/hands-on-knowledge/` for durable, practical lessons that future agents or developers are likely to need during implementation, debugging, verification, migration, recovery, or codebase orientation.

Expected homes:

| Destination | Purpose |
|---|---|
| `docs/hands-on-knowledge/entry-map.md` | Routing and search strategy. Keep it as a map, not a full index. |
| `docs/hands-on-knowledge/implementation/` | Reusable implementation patterns, migration notes, verification notes, integration practices, and maintained implementation references. |
| `docs/hands-on-knowledge/debug/` | Investigations, runbooks, known failure modes, recovery procedures, postmortems, platform traps, and diagnostic references. |
| `docs/top-level-knowledge/` | Stable project, architecture, product, domain, or technology-stack facts. |
| `AGENTS.md` or `CLAUDE.md` | Mandatory operating rules that must be seen in every session. Choose the repository's canonical agent entry file for the active host. |

Source material may come from conversation context, completed plans, handoffs, logs, code review notes, verification output, changed files, temporary notes, `docs/impl-plans/`, `docs/exchange/`, repo-root `exchange/`, or retrospectives. These are sources, not final homes.

## Routing

Split mixed input into small candidate knowledge items before routing. One request may route to multiple destinations.

Use `impl-knowledge-maintainer` when an item is primarily about:

- how code should be built, integrated, migrated, structured, or reused
- module boundaries, schema patterns, validation patterns, server/client separation, wrappers, adapters, or architecture-level implementation practices
- verified commands, test approaches, release checks, or verification paths that should guide future implementation
- package-specific behavior that shapes future code
- implementation retrospectives or preserved implementation references

Use `debug-knowledge-maintainer` when an item is primarily about:

- symptoms, diagnosis, root cause, remediation, or recovery
- known issues, recurring failure modes, platform/runtime traps, environment problems, or contract drift risks
- debug investigations, runbooks, postmortems, recovery procedures, or preserved logs with framing
- feature-to-code entry paths that matter most during diagnosis

Use both child skills when a session produced both implementation lessons and debug/recovery lessons. For example, a verified API schema refactor pattern plus a PDF preview 404 diagnosis should be split and routed to both maintainers.

Route outside the child skills when the item is not hands-on implementation or debug knowledge:

- Stable product, architecture, domain, milestone, or technology-stack facts belong in `docs/top-level-knowledge/`.
- Broad roadmap or milestone strategy belongs in `docs/epic-plans/` when the repository uses that taxonomy.
- Feature or module design decisions belong in `docs/func-design/`.
- Temporary coding plans belong in `docs/impl-plans/`.
- Mandatory agent/session rules belong in the repository's canonical agent entry file. Use `AGENTS.md` for Codex/OpenAI-agent-oriented projects and `CLAUDE.md` for Claude-oriented projects when that is the maintained instruction source.

Do not force top-level project context, product background, or ordinary planning content into implementation or debug knowledge.

## Workflow

1. Infer the source material from the prompt, conversation, files mentioned, changed paths, plans, handoffs, logs, or notes.
2. Confirm completion only when it is unclear whether the task, milestone, implementation, or debug investigation is done enough to preserve. Ask a short confirmation instead of curating unfinished work.
3. Split mixed material into small candidate knowledge items.
4. Classify each item as implementation, debug, both, top-level knowledge, mandatory rule, temporary planning, one-off, stale candidate, or unclear.
5. For implementation items, load `impl-knowledge-maintainer` and follow its workflow and references.
6. For debug items, load `debug-knowledge-maintainer` and follow its workflow and references.
7. For both-routed items, keep the implementation-facing lesson and the diagnostic/recovery lesson separate so each child skill can maintain the narrowest durable home.
8. Before changing maintained docs, search the relevant existing knowledge and prefer updating existing documents over creating new ones.
9. Evaluate whether `docs/hands-on-knowledge/entry-map.md` needs a routing update after any material change under `docs/hands-on-knowledge/`.
10. Report the result grouped by route.

The child skills own detailed metadata, curation rules, destination-specific decisions, and final document shape. This manager should not copy their reference files into its own instructions; load the relevant child skill when the route is known.

## Durability Gate

Preserve only knowledge likely to matter again:

- repeated implementation or debug pattern
- non-obvious runtime, platform, integration, or package behavior
- migration, refactor, verification, or recovery lesson
- known failure mode or root cause that future work could hit again
- codebase entry path that materially shortens future implementation or diagnosis
- project fact important enough to guide future planning or architecture decisions

Ignore one-off logs, ordinary status updates, facts obvious from current code/tests, and per-session notes that do not change future behavior.

## Final Report

When finishing a curation pass, report:

- implementation-routed items and the docs updated or created
- debug-routed items and the docs updated or created
- both-routed items and how they were split
- top-level or mandatory-rule items routed outside hands-on knowledge
- ignored one-offs or unfinished items
- whether `docs/hands-on-knowledge/entry-map.md` changed, and why

If no maintained docs changed, say so clearly and explain whether the material was one-off, already covered, unfinished, or better handled by another documentation layer.

## Examples

Input: `把这次 API schema refactor 的经验沉淀一下`

Route: `impl-knowledge-maintainer`

Reason: implementation/refactor lesson likely belongs under `docs/hands-on-knowledge/implementation/`.

Input: `把刚才排查 Azure Document Intelligence 失败的过程整理成 runbook`

Route: `debug-knowledge-maintainer`

Reason: diagnostic and recovery procedure belongs under `docs/hands-on-knowledge/debug/runbooks/`.

Input: `这次实现里发现了一个验证命令模式，也踩了一个 PDF preview 404 的坑，帮我沉淀`

Route: both

Reason: verification command pattern routes to implementation knowledge; PDF preview 404 diagnosis routes to debug knowledge.

Input: `把项目背景写进 top-level docs`

Route: `docs/top-level-knowledge/`

Reason: stable project context should not be forced into implementation or debug hands-on knowledge.
