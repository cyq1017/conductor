# Task Sizing Guide

> Not every task needs a full planning cycle. Size it first, then pick the right process.

## The Problem

AI agents default to "receive instruction → start coding". Without sizing, you either:
- **Over-process**: Full brainstorm + plan + TDD for a one-line fix (wasted 30 min)
- **Under-process**: Jump into a complex refactor without a plan (wasted 3 hours on wrong approach)

## The Task Startup Protocol

Before any work begins, the agent evaluates and reports:

```
1. My understanding of the goal: ____
2. Estimated files involved: ____
3. Estimated time: ____
4. Recommended size: S / M / L
5. Uncertainties: ____
```

**The human confirms before work begins.**

## Size Definitions

### S — Small (< 30 min, 1-2 files)

**Examples**: Fix a typo, update a config, add a comment, rename a variable.

**Process**: Just do it → test → commit → update HANDOFF.

**No brainstorming. No planning. No TDD ceremony.**

---

### M — Medium (1-3 hours, 3-5 files)

**Examples**: Add a new API endpoint, refactor a module, fix a multi-file bug.

**Process**: Brief plan (bullet list, not a doc) → execute → test → commit → HANDOFF.

---

### L — Large (> 3 hours, cross-module)

**Examples**: New feature, architecture change, major refactor.

**Process**: Full cycle — brainstorm → design doc → plan → TDD → review → HANDOFF.

---

## Proxy Metrics for Sizing

When you're not sure how to size a task, use these indirect indicators:

| Metric | Small | Medium | Large |
|--------|-------|--------|-------|
| Files involved | 1-2 | 3-5 | 6+ |
| Your familiarity | Done this before | Mostly familiar | First time |
| Reversibility | Easy git revert | Some risk | Hard to undo |
| Dependencies | Self-contained | Few dependencies | Cross-module |

## Escalation Rule

**Default to Small. Escalate when needed.**

If the agent starts working on what was sized as S but discovers it's actually complex:

```
"This is more complex than expected — it touches 5 files and has a dependency 
on module X. I recommend re-sizing to M and doing a brief plan. Proceed?"
```

The human decides whether to escalate or continue.
