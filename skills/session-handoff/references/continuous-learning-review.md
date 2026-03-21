# Continuous Learning Review

Use this reference only after Phase 1 is complete and only if the user explicitly asks to continue.

This is a manual review branch. It does not create or modify skills automatically.

## Output Structure

Produce exactly these sections:

### Candidate pattern
- Describe the potentially reusable workflow, judgment rule, or corrective pattern from the session.

### Why it may be reusable
- Explain any cross-project or cross-session value.
- Focus on stable process, not one-off file edits.

### Why it may not be reusable
- Call out repo-specific paths, local product assumptions, one-off bugs, or narrow context that weakens reuse.

### Recommendation
- Use exactly one of:
  - `extract into a new skill`
  - `fold into an existing skill`
  - `keep as project-specific guidance`
  - `do nothing`

## Decision Heuristics

Default to `do nothing` or `keep as project-specific guidance` when the pattern:

- depends on the current repository layout
- depends on local branch or worktree state
- is mostly about one bug rather than a repeatable method
- is better captured in project docs than in a reusable skill

Prefer `fold into an existing skill` when the pattern:

- changes how an existing skill should be used
- belongs inside skill governance or skill authoring
- overlaps heavily with `writing-skills`, `skill-creator`, or `continuous-learning`

Recommend `extract into a new skill` only when the pattern:

- solves a recurring class of problem
- has stable, repeatable steps
- would still make sense outside the current repository
- adds process or judgment, not just a one-time result

## Important Boundary

After giving the recommendation, stop and wait for user confirmation.

Do not:

- create a new skill
- edit an existing skill
- package any skill
- write the review into the handoff markdown
