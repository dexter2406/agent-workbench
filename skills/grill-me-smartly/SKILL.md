---
name: grill-me-smartly
description: Review a plan by running the grill-me skill in the main session while using a standing answer-only subagent to represent the user for codebase research and factual confirmation. The subagent must not use skills; it answers the main session's concrete questions from local investigation. Store compact answer notes under docs/exchange, then continue the grill-me decision tree with those answers.
---

# Grill Me Smartly

Use this skill to review a plan with a two-lane process:

- The main session runs the actual `grill-me` skill and owns the decision-tree interview.
- A standing subagent represents the user for answer gathering: it researches local files, confirms code facts, and answers the main session's concrete question.

Keep the subagent's detailed research in `docs/exchange` so the main session stays compact. The main session then uses those answers to continue `grill-me` and decide what still needs the real user's input.

## Loop Contract

This is a loop, not a one-shot review.

For each iteration:

1. Main session proposes exactly one `grill-me` question.
2. The same standing subagent answers that question when it can be researched locally.
3. Main session records the answer and marks only that decision as resolved.
4. Main session explicitly continues to the next `grill-me` question.

After a subagent answer, say the equivalent of: "This first decision is resolved; continue to the second decision." Do not frame a single answered question as the whole review being complete.

Only produce a final decision packet when one of these termination conditions is true:

- The decision tree has no remaining material branches.
- The next unresolved question requires the real user's preference, product intent, or risk tolerance.
- The user explicitly asks to stop and summarize.
- Further questions would be duplicates or low-value restatements of already resolved decisions.

## Subagent Lifecycle

Create or reuse one standing answer-only subagent for the whole review loop. Do not create a fresh subagent per question.

- Start the subagent before the first locally answerable `grill-me` question.
- Keep the same subagent open across all loop iterations so it preserves the plan context and prior answers.
- For each new question, send the new question to that same subagent.
- Close the subagent only after the loop reaches a termination condition and the main session has read or recorded the final answer note.
- If the subagent fails or loses context, explicitly state that a replacement is being opened and pass it the accumulated exchange note before continuing.

## Workflow

1. Confirm the review target.
   - Identify the plan being reviewed from the user's message, a specified file, or the current conversation.
   - If important context is available in local files, inspect it before asking.
   - Do not begin implementation while this review workflow is active.

2. Use the real `grill-me` skill in the main session.
   - Load and follow `skills/grill-me/SKILL.md`; do not approximate it as "`grill-me`-style".
   - Interview the plan relentlessly through a decision tree.
   - Ask one concrete question at a time.
   - If a question can be answered by exploring the codebase, answer it through investigation before asking the user.
   - Include the main session's recommended answer when there is enough evidence.

3. Open or reuse one standing answer-only subagent.
   - Use a subagent only when the user explicitly requested this workflow or otherwise authorized subagents.
   - Use the same subagent for every locally answerable question in the review loop.
   - Tell the subagent it represents the user only for factual/codebase answers requested by the main session.
   - Tell the subagent not to use any skills, even if a skill seems relevant.
   - Give it the plan, the exact current question, and any local paths or context it should inspect.
   - On later iterations, send only the next question plus any new context; do not spawn a new subagent just because the question changed.
   - Ask for a concise answer, supporting evidence, uncertainty, and whether the answer changes the next grill-me decision.
   - Do not ask it to classify question priority or make final irreversible decisions.

4. Decide whether the real user still needs to answer.
   - If the subagent's researched answer resolves the question, continue the `grill-me` decision tree in the main session.
   - Treat that response as the end of the current loop iteration, not the end of the skill.
   - Announce the transition clearly: the current decision is resolved, then move to the next decision.
   - If the answer depends on product intent, preference, risk tolerance, or facts not discoverable locally, ask the real user one question.
   - Do not convert the workflow into a batch priority review unless the user asks for that explicitly.

5. Record the subagent answer under `docs/exchange`.
   - Create a compact Markdown note in `docs/exchange/`, for example `docs/exchange/grill-me-smartly-YYYYMMDD-HHMMSS.md`.
   - Store the plan snapshot, main-session question, subagent answer, inspected evidence, uncertainty, and the main session's next decision.
   - Keep the file concise; its job is to preserve context without loading the full subagent thread into the main session.

6. Merge and return the decision.
   - Read the `docs/exchange` note before responding.
   - Combine the main session's `grill-me` review with the subagent's researched answers.
   - Return the user-facing decision packet with:
     - the current grill-me question or decision,
     - the answer gathered by the subagent, if any,
     - the main session's recommended answer or default,
     - what still needs the real user's decision,
     - the path to the exchange note.

## Review Note Format

When writing a temporary review note, use this minimal structure:

```markdown
# grill-me-smartly review

## Source
- Task: <one sentence>
- Source file/context: <path or current conversation>
- Created at: <ISO timestamp>

## Plan Snapshot
<short summary of the reviewed plan>

## Proposed Questions
| ID | Question | Main-session recommended answer |
| --- | --- | --- |
| Q1 | ... | ... |

## Subagent Answer
| ID | Answer | Evidence | Uncertainty |
| --- | --- | --- |
| Q1 | ... | ... | ... |

## Decision Packet
- Resolved locally: <questions or decisions>
- Needs real user: <questions or decisions>
- Recommended decision: <what to ask or decide now>
```

## Common Mistake

Do not stop after the first answered question. `grill-me` intentionally asks one question at a time, so a successful first answer means the loop should advance, not finish. Use completion language only after checking the termination conditions above.

Do not spawn one subagent per question. The subagent is standing for the entire review; per-question dispatch loses context and changes the intended workflow.

## Question Quality Bar

Good questions should:

- Name the exact decision being forced.
- Explain why the answer matters now.
- State the recommended answer when evidence is sufficient.
- Avoid asking for information already discoverable from local files, docs, git history, or available tools.
- Avoid bundles of unrelated questions unless producing a final decision packet.
