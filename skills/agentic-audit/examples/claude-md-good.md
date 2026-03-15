# Good CLAUDE.md Example

This is an example of a high-quality CLAUDE.md file. Use this as a reference when auditing.

---

```markdown
# Project: Payment Service API

## Overview
A Node.js REST API for processing payments. Uses Stripe for payment processing and PostgreSQL for persistence.

## Tech Stack
- Runtime: Node.js 20 + TypeScript
- Framework: Express 5
- Database: PostgreSQL 16 via Prisma ORM
- Testing: Vitest + Supertest
- Linting: ESLint + Prettier

## Agent Behavior Rules

### Before making changes
- Always read the file you are about to modify
- Check existing tests to understand expected behavior

### Code style
- Use async/await, never .then() chains
- All functions must have TypeScript types — no `any`
- Errors must use the custom `AppError` class from `src/errors.ts`

### Testing
- Every new function needs a unit test
- Integration tests live in `tests/integration/`
- Run `npm test` before marking any task complete

### Verification
Before claiming work is done, run:
1. `npm run lint` — must pass with 0 errors
2. `npm test` — all tests must pass
3. `npm run build` — must compile without errors

### Off-limits
- Never modify `prisma/migrations/` directly
- Never commit `.env` files
- Never use `process.exit()` in application code
```

---

## Why this is good

- **Clear project context** at the top
- **Specific, actionable rules** (no vague guidance)
- **Explicit verification steps** with exact commands
- **Hard boundaries** clearly stated
- **No contradictions** between rules
- **Tech stack is specific** (versions included)
