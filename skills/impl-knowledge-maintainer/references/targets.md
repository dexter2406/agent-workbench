# Implementation Knowledge Targets

Use the narrowest durable home:

| Destination | Use when |
|---|---|
| `docs/hands-on-knowledge/implementation/` | Maintained implementation-facing hands-on knowledge. |
| `docs/hands-on-knowledge/implementation/patterns/` | Reusable implementation pattern that should guide future code. |
| `docs/hands-on-knowledge/implementation/references/` | Preserved implementation background, evidence, retrospective, or supporting notes. |
| `docs/hands-on-knowledge/entry-map.md` | Search/routing strategy changes. Do not make it a full index. |
| `docs/hands-on-knowledge/debug/` | Lesson is primarily diagnosis, debugging, or recovery. |
| `docs/top-level-knowledge/` | Stable project, architecture, or tech-stack fact. |
| `AGENTS.md` | Mandatory operating rule that must be read every session. |

Typical implementation patterns:
- known-good module boundaries
- integration wrapper patterns
- validation or schema patterns
- server/client separation patterns
- verified testing or verification approaches
- migration patterns likely to repeat

Typical implementation references:
- curated temporary notes
- implementation retrospectives
- preserved command output with framing
- dependency or package notes
- supporting evidence for a pattern

Do not force debug lessons into implementation. Route diagnosis/recovery to `debug/`; promote stable facts or mandatory rules upward.
