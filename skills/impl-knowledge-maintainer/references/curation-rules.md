# Implementation Knowledge Curation Rules

## Split-Homes Gate

Before creating any new document, split candidate lessons into smaller knowledge items and search existing maintained knowledge for each item:

- `docs/hands-on-knowledge/implementation/`
- `docs/hands-on-knowledge/implementation/patterns/`
- `docs/hands-on-knowledge/implementation/references/`
- `docs/hands-on-knowledge/entry-map.md`
- `docs/hands-on-knowledge/debug/` if diagnostic or recovery-oriented
- `docs/top-level-knowledge/` if stable project/architecture fact

Prefer updating the narrowest existing document when the item concerns the same package, integration, runtime, feature surface, coding pattern, migration, or verification path; corrects an assumption; adds a caveat or migration step; or adds evidence to a recommendation.

A single pass may both update existing docs and create a new doc for uncovered knowledge. If you create a new doc, report which items had no existing home and which were merged.

## Durability Gate

Promote only lessons likely to matter again:

- repeated implementation pattern
- package-specific integration behavior
- migration or refactor lesson
- verification path that prevents future mistakes
- runtime constraint shaping implementation
- trap not obvious from current code

Ignore one-off logs, ordinary process notes, and facts obvious from current code/tests.

## Alignment Gate

Before trusting or updating a doc, check referenced files, functions, components, commands, behaviors, status claims, and runtime paths against current code. If stale, mark `stale-candidate` or rewrite.

## Action Order

Choose the first applicable action:

1. `ignore`
2. `update existing`
3. `create new`
4. `promote`
5. `route to debug`
6. `historical-only`
7. `archive`

## Entry-Map Gate

After creating, moving, or materially updating anything under `docs/hands-on-knowledge/`, evaluate `entry-map.md`.

Update it only when a new artifact becomes a common first stop, a new package/integration/runtime/workflow/pattern family appears, search terms would not find it, an old route is stale/vague, or the user asks why it was not updated.

If unchanged, state why, e.g. existing implementation route already covers the pattern.
