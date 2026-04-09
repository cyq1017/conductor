# Trust Calibration Framework

> How to know when to trust your AI agent — and when to double-check.

## The Problem

"I don't know what I don't know" is the original sin of AI-assisted development.

If you just drive the AI to work and walk away, you'll never know:
- Where your instructions were unclear
- Where the AI consistently makes mistakes
- Which domains the AI is reliable in vs. not

## The Four-Layer Trust Model

### Layer 1: Outcome Verification
**You don't need to understand the process — verify the result.**

- Does the code run?
- Do the tests pass?
- Does the deployment succeed?

Use this when: The task has clear, verifiable outcomes.

### Layer 2: Cross-Verification
**Use another agent to review.**

- Have Codex review Claude Code's output
- Have Antigravity do a second opinion on architecture decisions
- Compare answers from two different models

Use this when: High-stakes decisions, or domains you're unfamiliar with.

### Layer 3: Progressive Trust
**Start small, verify, then expand.**

- Try the agent's approach on one file first
- If it works, apply to the whole module
- If it fails, you've limited the blast radius

Use this when: First time working with an agent on a new type of task.

### Layer 4: Demand Explanation
**Don't accept what — ask why.**

- "Why did you choose Flask over FastAPI?"
- "What are the alternatives and trade-offs?"
- "What could go wrong with this approach?"

Use this when: You suspect the agent is pattern-matching rather than reasoning.

## Agent Trust Profile

Over time, build a trust profile for each agent by tracking errors:

```markdown
## Claude Code Trust Profile

### Reliable Areas ✅
- Code refactoring
- Test writing
- Documentation generation

### Caution Areas ⚠️
- transformers 5.x API migration (3 errors logged)
- Starts coding before confirming requirements (2 incidents)

### Unreliable Areas ❌
- Assumes external tools are available without checking (1 hallucination)
```

**Source**: Your AI Error Book. Every error logged is a data point for trust calibration.

## The Retrospective Loop

Trust isn't static. After each significant session:

1. **AI Review**: What did the AI do well? Where did it fail?
2. **Human Review**: Where were your instructions unclear? What could you have said better?
3. **Workflow Update**: Update CLAUDE.md rules, error book, and trust profile.

This is **Deliberate Practice with AI** — you're not just using AI, you're getting better at using AI.

## Template

See `templates/TRUST_PROFILE.md.template` and `templates/ERROR_BOOK.md.template`.
