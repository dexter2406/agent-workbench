# Implementation Knowledge Workflow

## Required Inputs

Infer or confirm:
- completed feature, refactor, integration, or plan
- runtime surface, package, module, or workflow involved
- files changed or inspected
- durable vs one-off implementation lessons
- existing implementation docs covering the topic

If completion is not confirmed, ask: `是否把这次已完成的实现 / plan 结果沉淀进 implementation knowledge？`

## Source Handling

Source material may start in `docs/impl-plans/`, `docs/exchange/`, `docs/exchange/handoffs/`, repo-root `exchange/`, ad-hoc notes, code review notes, verification logs, or retrospectives. These are sources, not final homes.

After curation, maintained implementation artifacts live under `docs/hands-on-knowledge/implementation/`. Keep temporary artifacts only if still useful; move preserved implementation references to `implementation/references/`.

## Steps

1. Read hands-on entry map, existing implementation patterns, references, feature contracts, and related top-level docs.
2. Inspect current code path before trusting docs.
3. Run split-homes gate.
4. Classify: mandatory rule, stable architecture fact, implementation pattern, reference, migration note, verification note, debug/recovery knowledge, stale candidate.
5. Normalize temporary source files into implementation destinations.
6. Apply the smallest useful update set.
7. Run entry-map gate.
8. Add or refresh metadata.
9. Mark historical notes explicitly.

## Final Reporting

Report updated docs, new docs, ignored one-offs, debug-routed items, and whether `entry-map.md` changed. If a new artifact was created without entry-map changes, explain why.

Bad outcomes: per-session permanent notes, new docs when existing ones fit, one-off logs as guidance, debug lessons forced into implementation docs, knowledge left in `exchange` or `impl-plans`, or AGENTS doing evaluation logic.
