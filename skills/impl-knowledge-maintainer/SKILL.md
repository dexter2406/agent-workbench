---
name: impl-knowledge-maintainer
description: Use when curating durable implementation lessons, reusable coding patterns, migration notes, verification notes, or hands-on implementation references after implementation work.
---

# Implementation Knowledge Maintainer

Maintain implementation lessons under `docs/hands-on-knowledge/implementation/`.

Hands-on knowledge is a reverse-indexed memory for future agents, not a forward design or implementation note. Preserve only experience that would help a future agent quickly recognize, search for, or avoid a non-obvious implementation trap after they hit a problem or feel uncertain.

Default flow: confirm the feature, refactor, integration, or plan is complete; identify what actually caused confusion, rework, false starts, or non-obvious verification effort; search existing implementation docs and `entry-map.md`; split lessons into small items; ignore one-offs and forward design details; update existing docs first; create only for uncovered durable traps or experience; then decide whether `entry-map.md` needs a routing update.

Do not preserve details that a normal implementation plan, feature design, test name, or obvious code reading would already cover. If a lesson is simply "what the code now does" or "what the plan required", route it to the feature design/impl plan or ignore it. Keep hands-on entries focused on symptoms, search terms, root causes, and the shortest path a future agent should take when the same class of problem appears.

Load references only when needed:
- `references/targets.md` for destination choices and promotion matrix.
- `references/curation-rules.md` for split-homes, durability, alignment, and entry-map gates.
- `references/metadata.md` when creating or refreshing maintained docs.
- `references/workflow.md` for required inputs, source handling, AGENTS interaction, and final reporting.
