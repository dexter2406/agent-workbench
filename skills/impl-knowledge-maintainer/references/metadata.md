# Implementation Knowledge Metadata

Every maintained implementation-knowledge document should carry:

```yaml
---
status: active
doc_type: implementation-pattern
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
- `implementation-pattern`
- `implementation-reference`
- `migration-note`
- `verification-note`
- `directory-guide`

`source_of_truth` should name where truth currently lives, e.g. `current code`, `current code + docs/top-level-knowledge/tech-stack.md`, or `historical implementation only`.

Do not invent richer metadata unless the repo already established it.
