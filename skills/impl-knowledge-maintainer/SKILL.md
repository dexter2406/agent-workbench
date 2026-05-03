---
name: impl-knowledge-maintainer
description: Use when curating durable implementation lessons, reusable coding patterns, migration notes, verification notes, or hands-on implementation references after implementation work.
---

# Implementation Knowledge Maintainer

Maintain implementation lessons under `docs/hands-on-knowledge/implementation/`.

Default flow: confirm the feature, refactor, integration, or plan is complete; search existing implementation docs and `entry-map.md`; split lessons into small items; ignore one-offs; update existing docs first; create only for uncovered durable lessons; then decide whether `entry-map.md` needs a routing update.

Load references only when needed:
- `references/targets.md` for destination choices and promotion matrix.
- `references/curation-rules.md` for split-homes, durability, alignment, and entry-map gates.
- `references/metadata.md` when creating or refreshing maintained docs.
- `references/workflow.md` for required inputs, source handling, AGENTS interaction, and final reporting.
