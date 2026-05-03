# Usage Examples

These examples show how `init-project-context` should behave in realistic repository discovery and context-closure sessions.

## Example 1: Very Vague New Project

### User Request

```text
This is an internal AI tool project. I need help figuring out what this repo is actually for before we build anything.
```

### Expected Behavior

1. Inspect the repository before asking questions.
2. Summarize confirmed facts briefly.
3. Identify the highest-impact missing context.
4. Ask one narrowing question about the current milestone or smallest useful closed loop.
5. Refuse to draft agent entry files until the project purpose and scope are concrete enough.
6. When ready, draft top-level knowledge under `docs/top-level-knowledge/`.

### Good Follow-Up Question

```text
I can see the repo structure, but the project itself is still loosely defined. What is the smallest meaningful thing this repository is supposed to deliver first?
```

### What Not To Do

- Do not ask five broad questions at once.
- Do not start drafting instruction files from "AI tool project" alone.
- Do not create implementation plans before project meaning and milestone are stable.

## Example 2: Course Project With Unclear Scope

### User Request

```text
This is a course project for a cloud-based web app. Help me initialize the project context.
```

### Expected Behavior

1. Discover the current repository state and any existing concept docs.
2. Do not ask for technical facts already visible in the repository.
3. Ask what the project is for, how it will be evaluated, and what must be delivered.
4. Draft `docs/top-level-knowledge/project-context.md` and `docs/top-level-knowledge/tech-stack.md`.
5. Add short definitional README files for the default `docs/` taxonomy if creating the structure.
6. Treat agent instruction files as optional follow-up output.

### Good Follow-Up Question

```text
I can already see that this is a cloud web app repo, but I still need the real boundary for the assignment. What are the required features, and what is intentionally out of scope for the course project?
```

### What Not To Do

- Do not jump straight into agent rules if the project itself is still fuzzy.
- Do not mistake candidate stack notes for finalized implementation truth.
- Do not use the old investigation filename; the default file is `tech-stack.md`.

## Example 3: User Pushes For Immediate Agent Files

### User Request

```text
Just write AGENTS.md and a separate CLAUDE.md directly.
```

### Expected Behavior

1. Check whether the repository has enough stable context.
2. If not, explain why direct drafting would lock in bad assumptions about the project.
3. Continue discovery until project purpose, scope, and candidate technical direction are strong enough.
4. Choose one canonical agent instruction file only after the user confirms the main host or the repo makes it obvious.
5. Make additional host files point to the canonical file instead of duplicating content.

### Good Response Shape

```text
The repository does not yet have enough stable project context for safe instruction drafting. I need to close the project purpose, required scope, and candidate technical direction first so the files do not encode weak assumptions.
```

### What Not To Do

- Do not comply immediately when the project description is still fuzzy.
- Do not invent rules that the repository and user have not established.
- Do not maintain parallel `AGENTS.md` and `CLAUDE.md` content when a link or pointer would do.
- Do not assume `AGENTS.md` must be canonical for every project.

## Example 4: Progressive Disclosure In Agent Instructions

### User Request

```text
Make the agent instructions lighter. They should say where docs live, not force every agent to read everything first.
```

### Expected Behavior

1. Keep agent entry files concise: scope, documentation index, commands, and rules.
2. Point to the four `docs/` directories as a progressive-disclosure index.
3. Avoid detailed project explanations in the agent file.
4. Let agents choose which docs to open based on the task.

### Good Agent Instruction Pattern

```markdown
## Documentation Index

Use these directories as a progressive-disclosure index. Open only the docs relevant to the current task:

- `docs/top-level-knowledge/` — stable project context and architecture knowledge.
- `docs/epic-plans/` — epic-level plans and milestone strategy.
- `docs/func-design/` — focused feature/module designs.
- `docs/impl-plans/` — temporary coding plans; archive after acceptance.
```

### What Not To Do

- Do not say "Before planning or implementing, read all docs."
- Do not duplicate the contents of `project-context.md` or `tech-stack.md` in the agent file.
- Do not turn directory README files into manual file indexes.

## Example 5: Claude-First Or Codex-First Canonical File

### User Request

```text
This project is mostly driven by Claude, but Codex should also understand the rules.
```

### Expected Behavior

1. Use `CLAUDE.md` as the canonical body if the user confirms Claude-first usage.
2. Create `AGENTS.md` as a symlink, hard link, or short pointer to `CLAUDE.md`.
3. Keep only one maintained instruction body.

### Alternate Codex-First Behavior

For a Codex-first project, use `AGENTS.md` as the canonical body and make `CLAUDE.md` point to it only if Claude compatibility is required.

### What Not To Do

- Do not create two full instruction files with copied content.
- Do not create compatibility aliases for hosts the user does not use.

## Example 6: Temporary Exchange Material

### User Request

```text
I need somewhere to drop temporary snippets and notes while we work through this migration.
```

### Expected Behavior

1. Use a root-level `exchange/` directory for temporary information exchange.
2. Add `exchange/` to `.gitignore`.
3. Move durable information into the appropriate `docs/` directory once it becomes part of project knowledge or planning.

### What Not To Do

- Do not treat `exchange/` as long-term documentation.
- Do not link agent instructions to `exchange/` as a stable source of truth.

## Stop Condition

Instruction drafting is allowed only when all of these are true:

- The current project purpose is explicit.
- The primary users or operators are explicit.
- The current milestone is explicit.
- The required deliverables are explicit.
- In-scope / out-of-scope is explicit enough for planning.
- There is at least a provisional candidate technical direction, or an explicit statement that it is still open.
- The documentation taxonomy is clear enough for future docs to be placed predictably.
- Future planning would not depend on repeated oral clarification of core context.
