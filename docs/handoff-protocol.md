# Multi-Agent Handoff Protocol

> How to pass context between AI coding sessions without losing information.

## The Problem

Every time you start a new AI coding session, you waste 5-10 minutes re-explaining what happened before. Decisions get lost. Mistakes get repeated. Context evaporates.

## The Protocol

### At Session End: Write HANDOFF.md

Every project maintains a `HANDOFF.md` at its root. Before ending a session, the agent writes:

```markdown
## YYYY-MM-DD

- **done**: What was completed this session
- **blocked**: What's stuck and why (skip if none)
- **decisions**: Key choices made and alternatives rejected
- **pitfall**: Mistakes made — don't repeat these (skip if none)
- **next**: Recommended next steps, in priority order
```

### Rules

1. **500 token max** — Force compression. If you can't summarize in 500 tokens, you don't understand what you did.
2. **Record negative decisions** — "Tried Flask, rejected because X" prevents the next session from re-exploring dead ends.
3. **Pitfalls are gold** — Every mistake recorded saves future time. Include error messages, wrong assumptions, API quirks.
4. **Next steps are ordered** — Don't list 10 things. List 1-3, in priority order.

### At Session Start: Load Context

The agent reads HANDOFF.md first, then confirms understanding before working:

```
I've read the handoff. Last session you completed X, and the recommended 
next step is Y. The key constraint is Z. Should I proceed with Y?
```

## Multi-Project Coordination

When managing multiple projects with a central hub (e.g., Obsidian/Orbit):

```
Project A ──HANDOFF.md──→ Central Hub ──adjustments──→ Project A
Project B ──HANDOFF.md──→ Central Hub ──adjustments──→ Project B
Project C ──HANDOFF.md──→ Central Hub ──adjustments──→ Project C
```

The central hub:
1. Reads all project HANDOFFs daily
2. Discusses priorities with the human
3. Writes "central adjustments" back to each project (priority changes, new requirements, cross-project dependencies)

## Template

See `templates/HANDOFF.md.template` for a ready-to-use template.
