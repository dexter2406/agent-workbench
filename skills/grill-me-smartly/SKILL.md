---
name: grill-me-smartly
description: Review a plan by using the grill-me skill in the main session, asking a standing subagent to judge each proposed question as "非常有必要" or "需要再讨论" on behalf of the user, writing the subagent's classification notes under docs/exchange to save main-session context, and finally returning a combined decision packet to the user. Use when the user asks to review a plan with this exact workflow, mentions "grill-me-smartly", or asks for grill-me review plus subagent priority judgment and docs/exchange recording.
---

# Grill Me Smartly

Use this skill to review a plan with a two-lane process:

- The main session performs `grill-me`-style review and proposes sharp questions.
- A standing subagent acts as the user's first-pass filter, classifying each question as `非常有必要` or `需要再讨论`.

Keep the subagent's detailed reasoning in `docs/exchange` so the main session stays compact. Return the final decision packet to the user after combining the main-session review and subagent judgment.

## Workflow

1. Confirm the review target.
   - Identify the plan being reviewed from the user's message, a specified file, or the current conversation.
   - If important context is available in local files, inspect it before asking.
   - Do not begin implementation while this review workflow is active.

2. Use `grill-me` behavior in the main session.
   - Review the plan relentlessly through a decision tree.
   - Generate concrete questions that expose unclear goals, scope, dependencies, risks, acceptance criteria, rollout, rollback, and verification.
   - Ask questions one at a time when directly interacting with the user.
   - Include the main session's recommended answer when there is enough evidence.

3. Open or reuse a standing subagent as the user's first-pass judge.
   - Use a subagent only when the user explicitly requested this workflow or otherwise authorized subagents.
   - Tell the subagent to classify proposed questions as `非常有必要` or `需要再讨论`.
   - Ask it to act on behalf of the user only for triage, not to make final irreversible decisions.
   - Give the subagent the plan, the proposed questions, and the classification rule; do not leak the expected result.

4. Apply this classification rule.
   - `非常有必要`: the question must be answered before a decision because it can change the plan, scope, architecture, data model, API contract, security posture, rollout strategy, acceptance criteria, or implementation order.
   - `需要再讨论`: the question is useful but can be deferred, handled by a reversible default, or discussed after the next decision.

5. Record the subagent result under `docs/exchange`.
   - Create a compact Markdown note in `docs/exchange/`, for example `docs/exchange/grill-me-smartly-YYYYMMDD-HHMMSS.md`.
   - Store the plan snapshot, proposed questions, subagent classifications, short reasons, and recommended final decision.
   - Keep the file concise; its job is to preserve context without loading the full subagent thread into the main session.

6. Merge and return the decision.
   - Read the `docs/exchange` note before responding.
   - Combine the main session's `grill-me` review with the subagent's classifications.
   - Return the user-facing decision packet with:
     - questions that are `非常有必要`,
     - questions that `需要再讨论`,
     - recommended answers or defaults,
     - the final decision needed from the user,
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

## Subagent Classification
| ID | Classification | Reason |
| --- | --- | --- |
| Q1 | 非常有必要 | ... |
| Q2 | 需要再讨论 | ... |

## Decision Packet
- 非常有必要: <questions or decisions>
- 需要再讨论: <questions or decisions>
- Recommended decision: <what to ask or decide now>
```

## Question Quality Bar

Good questions should:

- Name the exact decision being forced.
- Explain why the answer matters now.
- State the recommended answer when evidence is sufficient.
- Avoid asking for information already discoverable from local files, docs, git history, or available tools.
- Avoid bundles of unrelated questions unless producing a final decision packet.
