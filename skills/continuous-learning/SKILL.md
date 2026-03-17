---
name: continuous-learning
description: Automatically extract reusable patterns from Claude Code sessions and save them as learned skills for future use.
origin: ECC
---

# Continuous Learning Skill

Automatically evaluates Claude Code sessions on end to extract reusable patterns that can be saved as learned skills.

The default path is still end-of-session extraction through a Stop hook. A secondary manual path is also valid when the user wants to pause mid-session, review what just happened, and decide whether a reusable pattern is worth extracting before the session ends.

## When to Activate

- Setting up automatic pattern extraction from Claude Code sessions
- Configuring the Stop hook for session evaluation
- Reviewing the current or recent session manually to decide whether anything should become a reusable skill
- Reviewing or curating learned skills in `~/.claude/skills/learned/`
- Adjusting extraction thresholds or pattern categories
- Comparing v1 (this) vs v2 (instinct-based) approaches

## How It Works

This skill runs as a **Stop hook** at the end of each session:

1. **Session Evaluation**: Checks if session has enough messages (default: 10+)
2. **Pattern Detection**: Identifies extractable patterns from the session
3. **Skill Extraction**: Saves useful patterns to `~/.claude/skills/learned/`

## Manual Session Review

Use this branch when the user asks to review the current session before it ends, or asks whether something that just happened is reusable enough to become a skill.

This is a lightweight branch, not a replacement for the Stop-hook flow:
- it does not require hook setup
- it does not require full automatic extraction
- it can end with "nothing worth extracting"

### When to use the manual branch

- The user says things like "can this be turned into a skill?" or "anything reusable from this session?"
- A session has produced a repeatable workflow, decision pattern, or corrective rule and the user wants to assess it immediately
- The session is still in progress, so waiting for the Stop hook is awkward

### Manual review output

For a manual review, produce a short assessment with:
1. **Candidate pattern**: what reusable behavior might exist
2. **Why it may be reusable**: cross-project or cross-session value
3. **Why it may not be reusable**: signs it is project-specific, one-off, or too narrow
4. **Recommendation**:
   - extract into a skill
   - fold into an existing skill
   - keep as project-specific guidance
   - do nothing

When the session is about editing skills themselves, also classify whether the pattern is:
- a new standalone skill candidate
- a governance sub-flow that should fold into an existing skill
- project-local guidance only

### Manual review heuristic

Treat a session pattern as a skill candidate only if most of these are true:
- it solved a recurring class of problem, not a one-off repo quirk
- the steps are stable enough to describe as a repeatable workflow
- the pattern would still make sense in a different repository
- the value is in judgment or process, not just a single file edit

Treat it as **not** worth extracting when:
- it is just ordinary project setup with no reusable insight
- it depends on repo-specific paths, naming, or local politics
- the "pattern" is really just a result, not a repeatable method
- the right home is an existing project file such as `AGENTS.md`

Treat it as a **fold-into-existing-skill** candidate when:
- the pattern governs how an existing skill family should be edited or validated
- the right home is an authoring or maintenance skill such as `writing-skills`
- creating a standalone skill would duplicate discovery surface and split one workflow across multiple entrypoints

### Skill-Governance Pattern

One common manual-review outcome is a `skill-governance pattern`.

Use this label when a session produces a reusable way to maintain or tighten skills themselves, for example:
- deciding when a skill edit changes canonical behavior
- reviewing whether compatibility wording has been fully removed
- distinguishing legacy read compatibility from supported execution paths

Default recommendation for `skill-governance pattern`:
- fold into an existing skill
- prefer `writing-skills` unless the pattern clearly belongs elsewhere
- do not create a standalone skill unless the workflow is broader than skill authoring

### Relationship to extraction

If the manual review concludes that a pattern is worth keeping:
- either extract it immediately into a draft skill
- or record the recommendation so the end-of-session flow can extract it later with better context

If the manual review concludes nothing is worth extracting, say so plainly and stop.

## Configuration

Edit `config.json` to customize:

```json
{
  "min_session_length": 10,
  "extraction_threshold": "medium",
  "auto_approve": false,
  "learned_skills_path": "~/.claude/skills/learned/",
  "patterns_to_detect": [
    "error_resolution",
    "user_corrections",
    "workarounds",
    "debugging_techniques",
    "project_specific"
  ],
  "ignore_patterns": [
    "simple_typos",
    "one_time_fixes",
    "external_api_issues"
  ]
}
```

## Pattern Types

| Pattern | Description |
|---------|-------------|
| `error_resolution` | How specific errors were resolved |
| `user_corrections` | Patterns from user corrections |
| `workarounds` | Solutions to framework/library quirks |
| `debugging_techniques` | Effective debugging approaches |
| `project_specific` | Project-specific conventions |
| `skill_governance` | Reusable patterns for creating, editing, and tightening skills |

## Hook Setup

Add to your `~/.claude/settings.json`:

```json
{
  "hooks": {
    "Stop": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "~/.claude/skills/continuous-learning/evaluate-session.sh"
      }]
    }]
  }
}
```

## Why Stop Hook?

- **Lightweight**: Runs once at session end
- **Non-blocking**: Doesn't add latency to every message
- **Complete context**: Has access to full session transcript

## Why Manual Review Exists

- **Good for mid-session reflection**: lets the user review a workflow before the session ends
- **Good for curation**: helps distinguish reusable process from project-specific cleanup
- **Lower ceremony**: useful when the user wants a quick judgment rather than full automatic extraction

## Related

- [The Longform Guide](https://x.com/affaanmustafa/status/2014040193557471352) - Section on continuous learning
- `/learn` command - Manual pattern extraction mid-session

---

## Comparison Notes (Research: Jan 2025)

### vs Homunculus

Homunculus v2 takes a more sophisticated approach:

| Feature | Our Approach | Homunculus v2 |
|---------|--------------|---------------|
| Observation | Stop hook (end of session) | PreToolUse/PostToolUse hooks (100% reliable) |
| Analysis | Main context | Background agent (Haiku) |
| Granularity | Full skills | Atomic "instincts" |
| Confidence | None | 0.3-0.9 weighted |
| Evolution | Direct to skill | Instincts → cluster → skill/command/agent |
| Sharing | None | Export/import instincts |

**Key insight from homunculus:**
> "v1 relied on skills to observe. Skills are probabilistic—they fire ~50-80% of the time. v2 uses hooks for observation (100% reliable) and instincts as the atomic unit of learned behavior."

### Potential v2 Enhancements

1. **Instinct-based learning** - Smaller, atomic behaviors with confidence scoring
2. **Background observer** - Haiku agent analyzing in parallel
3. **Confidence decay** - Instincts lose confidence if contradicted
4. **Domain tagging** - code-style, testing, git, debugging, etc.
5. **Evolution path** - Cluster related instincts into skills/commands

See: `docs/continuous-learning-v2-spec.md` for full spec.
