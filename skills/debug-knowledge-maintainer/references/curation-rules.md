# Debug Knowledge Curation Rules

## Split-Homes Gate

Before creating any new document, split candidate lessons into smaller knowledge items and search existing maintained knowledge for each item:

- `docs/hands-on-knowledge/debug/`
- `docs/hands-on-knowledge/debug/runbooks/`
- `docs/hands-on-knowledge/debug/investigations/`
- `docs/hands-on-knowledge/debug/references/`
- `docs/hands-on-knowledge/implementation/`
- `docs/hands-on-knowledge/entry-map.md`
- `docs/known-issues/` if the repository still uses it

Prefer updating the narrowest existing document when the item concerns the same integration, runtime, error family, feature surface, runbook, or investigation; corrects an assumption; adds symptom/cause/remediation; or adds verification evidence.

A single pass may both update existing docs and create a new doc for uncovered knowledge. If you create a new doc, report which items had no existing home and which were merged.

## Durability Gate

Promote only lessons likely to matter again:

- repeated failure mode
- platform/runtime limitation
- complex feature entry path
- known contract drift risk
- verification that prevents future mistakes

Ignore one-off logs, ordinary process notes, and facts obvious from current code/tests.

## Alignment Gate

Before trusting or updating a doc, check referenced files, functions, behaviors, status claims, and runtime paths against current code. If stale, mark `stale-candidate` or rewrite.

## Action Order

Choose the first applicable action:

1. `ignore`
2. `update existing`
3. `create new`
4. `promote`
5. `historical-only`
6. `archive`

## Entry-Map Gate

After creating, moving, or materially updating anything under `docs/hands-on-knowledge/`, evaluate `entry-map.md`.

Update it only when a new artifact becomes a common first stop, a new debug surface/package/integration/runtime/error family appears, search terms would not find it, an old route is stale/vague, or the user asks why it was not updated.

If unchanged, state why, e.g. existing Lark Base route already covers the runbook.
