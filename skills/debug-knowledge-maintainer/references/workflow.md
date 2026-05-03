# Debug Knowledge Workflow

## Required Inputs

Infer or confirm:
- completed debug task or plan milestone
- feature or runtime surface involved
- files changed or inspected
- durable vs one-off lessons
- existing debug docs covering the topic

If completion is not confirmed, ask: `是否把这次已完成的 debug / plan 结果沉淀进 debug knowledge？`

## Source Handling

Source material may start in `docs/impl-plans/`, `docs/exchange/`, `docs/exchange/handoffs/`, repo-root `exchange/`, ad-hoc notes, structured investigations, raw logs, or retrospectives. These are sources, not final homes.

After curation, maintained debug artifacts live under `docs/hands-on-knowledge/debug/`. Keep temporary artifacts only if still useful; move preserved debug references to `debug/references/`.

## Steps

1. Read relevant feature contract, hands-on entry map, existing debug investigations, runbooks, references, and known-issues notes.
2. Inspect current code path before trusting docs.
3. Run split-homes gate.
4. Classify: durable rule, feature entry knowledge, postmortem, runbook, stale candidate, investigation, reference-only retrospective.
5. Normalize temporary source files into debug destinations.
6. Apply the smallest useful update set.
7. Run entry-map gate.
8. Add or refresh metadata.
9. Mark historical notes explicitly.

## Final Reporting

Report updated docs, new docs, ignored one-offs, and whether `entry-map.md` changed. If a new artifact was created without entry-map changes, explain why.

Bad outcomes: per-session permanent notes, new docs when existing ones fit, one-off logs as guidance, knowledge left in `exchange` or `impl-plans`, or AGENTS doing evaluation logic.
