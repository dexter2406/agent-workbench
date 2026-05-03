---
name: session-handoff
description: Summarize the current session into a reusable handoff when the user asks to summarize this session, save context to disk, generate a handoff, migrate context into a new session, or整理当前进度/坑/后续. Use this whenever the user wants a session handoff artifact or wants context preserved before switching to a fresh conversation. After writing the handoff file, return a continuation prompt in chat instead of creating a second prompt file.
---

# Session Handoff

Create a durable handoff for the current session so a fresh conversation can continue with minimal re-discovery.

This skill has two phases:

1. Phase 1: write a single handoff markdown file and then return a continuation prompt in chat
2. Phase 2: only if the user explicitly wants to continue, perform a manual `continuous-learning` style review about whether this session produced a reusable skill pattern

Do not merge these phases. The handoff file is the default deliverable. The skill-extraction discussion is optional and happens only after the handoff is finished.

## When To Use This Skill

Use this skill when the user:

- asks to summarize the current session
- asks to save current context to disk
- asks for a handoff before opening a new session
- asks to migrate progress into a fresh conversation
- asks to整理当前进度、遇到的坑、完成状态、后续动作
- asks whether the session produced anything worth turning into a skill, but also needs a saved handoff first

## Example Triggers

These are representative prompts that should trigger this skill:

- `总结这个 session，把当前目标、完成状态、踩过的坑和后续动作落盘，我要切到新会话继续。`
- `帮我做一个 handoff，把当前上下文存到仓库里，然后给我一段能直接发到新 session 的提示词。`
- `把这次对话整理成 context handoff，我之后要在新会话继续 debug。`
- `先把当前进度和未验证项写成 handoff，再看看这次 session 有没有值得沉淀成 skill 的模式。`

These are near-misses that should not automatically route here:

- `帮我总结这份文档。`
- `把这个 bug 的根因写成 issue。`
- `帮我写一个新技能。`

## Phase 1: Write The Handoff

### Output location

By default, write the handoff file under the current repository root:

`docs/exchange/handoffs/session-handoff-YYYYMMDD-HHMM.md`

If the user explicitly provides another destination, follow that instead.

If the current repository is not a reasonable place to write the file, explain the issue briefly and use the user-specified path or ask for one only if no safe default exists.

### Required file structure

Read [handoff-template.md](D:\CodeSpace\agent-workbench\skills\session-handoff\references\handoff-template.md) before drafting the file. The handoff markdown must include exactly these sections:

- `# Session Handoff`
- `## Current Goal`
- `## Completion Status`
- `## What Changed`
- `## Pitfalls And Resolutions`
- `## Open Issues`
- `## Next Recommended Actions`
- `## Useful References`

The file must capture:

- the current goal and why the work matters
- what is finished, partially finished, or not finished
- what changed in code, logic, UI, docs, or workflow
- what bugs or pitfalls were encountered, their root causes, and how they were resolved
- what remains unverified or still needs human confirmation
- what a new session should do first

### Exclusions

Do not include any of the following inside the handoff markdown:

- `Continuous Learning Review`
- `Manual Alignment Needed`
- any recommendation about whether to create a new skill
- any automatic extraction or governance discussion

## Continuation Prompt In Chat

After the handoff file is written, read [continuation-prompt-template.md](D:\CodeSpace\agent-workbench\skills\session-handoff\references\continuation-prompt-template.md) and return a continuation prompt directly in chat.

Do not create a second file for the prompt.

The continuation prompt must include:

- the handoff file path
- the current goal
- the current status
- the must-read files
- the first recommended action
- a clear instruction to verify the current state before continuing implementation
- any open issues that the next session should confirm before changing code

## Phase 2: Optional Manual Review

Only enter this phase if the user explicitly asks to continue after Phase 1 is complete.

In Phase 2, read [continuous-learning-review.md](D:\CodeSpace\agent-workbench\skills\session-handoff\references\continuous-learning-review.md) and produce a structured manual review. This phase is advisory only.

Allowed recommendation values:

- `extract into a new skill`
- `fold into an existing skill`
- `keep as project-specific guidance`
- `do nothing`

Do not create, edit, or package any skill as part of this phase unless the user separately approves that next step.

## Workflow

1. Gather the current session facts from conversation history and the workspace.
2. Identify the current goal, actual completion state, resolved issues, unresolved issues, and recommended next action.
3. Write the handoff markdown file using the required template.
4. Report the saved file path.
5. Return the continuation prompt in chat.
6. Stop unless the user explicitly asks to continue into manual skill-candidate review.

## Quality Bar

- Prefer concrete facts over vague summaries.
- Distinguish verified work from assumed work.
- Name exact files, commands, or verification gaps when they matter.
- Keep the handoff useful for a new session that has not seen the original conversation.
- If the session involved debugging, preserve the bug, root cause, fix, and any residual risk.

## Prohibited Behavior

Do not:

- silently skip the file write
- write a prompt file instead of returning the prompt in chat
- fold Phase 2 analysis into the handoff markdown
- auto-run `continuous-learning` extraction hooks
- auto-create or auto-edit any additional skill
- pretend verification happened if it did not
