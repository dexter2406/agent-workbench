# Bad CLAUDE.md Examples — Anti-Patterns

Examples of poor CLAUDE.md configurations with analysis of what's wrong.

---

## Anti-Pattern 1: Vague aspirational rules

```markdown
# My Project

Be helpful. Write clean code. Follow best practices. Make sure everything works.
Don't break anything.
```

**Problems:**
- [CRITICAL] Zero actionable instructions — the agent has no idea what "clean" means here
- [CRITICAL] No tech stack information
- [CRITICAL] No verification steps
- [WARNING] "Don't break anything" is not a rule, it's a wish

---

## Anti-Pattern 2: Contradictory rules

```markdown
## Rules
- Always ask the user before making any file changes
- Work autonomously and complete tasks without interrupting the user
- Get confirmation before each step
- Complete the full implementation in one pass
```

**Problems:**
- [CRITICAL] Rules 1 & 2 directly contradict each other
- [CRITICAL] Rules 3 & 4 directly contradict each other
- The agent will behave unpredictably depending on which rule it applies

---

## Anti-Pattern 3: Too much irrelevant context

```markdown
# Project History

This project was started in 2019 by our team of 5 engineers. We originally used React
but switched to Vue in 2021 after a long debate. The CEO wanted us to use Angular but
we convinced him Vue was better. We use AWS because our DevOps lead prefers it.
In Q3 2022 we had a major incident with the database...

[500 more lines of history]

## Rules
- Write good code
```

**Problems:**
- [CRITICAL] Useful rules are buried in irrelevant history
- [WARNING] Wastes context window on non-actionable information
- [WARNING] Agent may hallucinate rules based on the narrative

---

## Anti-Pattern 4: Security risks

```markdown
## Environment
- Database password: prod123
- API key: sk-abc123xyz
- Use sudo when you need to install things
```

**Problems:**
- [CRITICAL] Never put secrets in CLAUDE.md — it gets committed to git
- [CRITICAL] `sudo` permissions are dangerously broad

---

## Anti-Pattern 5: No verification

```markdown
## Development
- Write the feature
- Make sure tests pass
- You're done!
```

**Problems:**
- [WARNING] "Make sure tests pass" — how? What command?
- [WARNING] No build verification
- [WARNING] Agent will claim completion without actually verifying

**Fix:**
```markdown
## Verification (required before completion)
Run: `npm test && npm run build`
Both must exit with code 0.
```

---

## Anti-Pattern 6: Mixing concerns

```markdown
The project uses TypeScript. Always be polite. We use PostgreSQL. Don't use var.
The database is on port 5432. Always ask before deleting. We have Redis for caching.
Never use console.log in production. The Redis port is 6379. Be thorough.
```

**Problems:**
- [WARNING] Rules and facts are interleaved — hard to parse
- [WARNING] No structure makes it easy to miss important rules
- [SUGGESTION] Group into: Tech Stack, Behavior Rules, Restrictions
