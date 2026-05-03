# Debug Knowledge Targets

Use the narrowest durable home:

| Destination | Use when |
|---|---|
| `docs/hands-on-knowledge/debug/` | Maintained debug entrypoints and feature-to-code maps. |
| `docs/hands-on-knowledge/debug/investigations/` | Reviewed debug investigation with a conclusion. |
| `docs/hands-on-knowledge/debug/runbooks/` | Repeatable debug or recovery procedure. |
| `docs/hands-on-knowledge/debug/references/` | Preserved debug background, logs, retrospectives, or evidence. |
| `docs/hands-on-knowledge/entry-map.md` | Search/routing strategy changes. Do not make it a full index. |
| `docs/hands-on-knowledge/implementation/` | Durable implementation practice, not diagnosis/recovery. |
| `docs/top-level-knowledge/` | Stable project, architecture, or tech-stack fact. |
| `AGENTS.md` | Mandatory operating rule that must be read every session. |
| `docs/known-issues/` | Historical reference only unless the repository still uses it actively. |

Typical debug investigations:
- `investigate-<slug>.md`
- debt review notes with conclusions
- reviewed debugging investigations

Typical debug runbooks:
- local webhook troubleshooting
- API connectivity recovery
- cache/session diagnosis
- known verification sequences

Typical debug references:
- retrospectives
- curated temporary notes
- preserved logs with framing
- imported temp artifacts that should remain together

Do not force non-debug lessons into debug. Route implementation practice to `implementation/`; promote stable facts or mandatory rules upward.
