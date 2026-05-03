---
name: debug-knowledge-maintainer
description: Use when curating durable debug lessons, known issues, investigations, runbooks, postmortems, or debug entry maps after debugging or an implementation milestone.
---

# Debug Knowledge Maintainer

Maintain debug lessons under `docs/hands-on-knowledge/debug/`.

Default flow: confirm the debug task or milestone is complete, search existing debug docs and `entry-map.md`, split lessons into small items, ignore one-offs, update existing docs first, create only for uncovered durable lessons, then decide whether `entry-map.md` needs a routing update.

Load references only when needed:
- `references/targets.md` for destination choices and promotion matrix.
- `references/curation-rules.md` for split-homes, durability, alignment, and entry-map gates.
- `references/metadata.md` when creating or refreshing maintained docs.
- `references/workflow.md` for required inputs, source handling, AGENTS interaction, and final reporting.
