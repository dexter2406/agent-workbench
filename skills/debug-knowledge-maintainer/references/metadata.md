# Debug Knowledge Metadata

Every maintained debug-knowledge document should carry:

```yaml
---
status: active
doc_type: investigation
source_of_truth: current code
last_verified_at: YYYY-MM-DD
---
```

`status` values:
- `active`
- `historical`
- `stale-candidate`
- `archived`

`doc_type` values:
- `debug-entry-map`
- `investigation`
- `postmortem`
- `runbook`
- `platform-note`
- `directory-guide`

`source_of_truth` should name where truth currently lives, e.g. `current code`, `current code + AGENTS.md`, or `historical investigation only`.

Do not invent richer metadata unless the repo already established it.
