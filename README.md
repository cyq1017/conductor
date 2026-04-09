<div align="center">

# 🎵 Conductor

**A framework for humans who orchestrate multiple AI coding agents.**

Structured handoff · Trust calibration · Continuous improvement

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-green.svg)](https://www.python.org)

**English** · [中文](README_zh.md)

</div>

---

## Supported AI Coding Agents

<table>
<tr>
<td align="center"><b>Claude Code</b><br/>Anthropic</td>
<td align="center"><b>Cursor</b><br/>AI IDE</td>
<td align="center"><b>GitHub Copilot</b><br/>Chat</td>
<td align="center"><b>Codex CLI</b><br/>OpenAI</td>
</tr>
<tr>
<td align="center"><b>Windsurf</b><br/>Codeium</td>
<td align="center"><b>Antigravity</b><br/>Google DeepMind</td>
<td align="center"><b>Gemini CLI</b><br/>Google</td>
<td align="center"><b>Kimi Code</b><br/>Moonshot AI</td>
</tr>
<tr>
<td align="center"><b>Aider</b><br/>Open Source CLI</td>
<td align="center"><b>Continue</b><br/>Open Source Plugin</td>
<td align="center" colspan="2"><i>+ any tool that reads/writes files</i></td>
</tr>
</table>

> Conductor is file-protocol based — any AI coding tool that can read and write files is compatible.

---

## The Problem

You're running Claude Code in one terminal, Cursor in another, maybe Codex for review — all on different projects. By end of day:

- 🤯 You can't remember what each agent decided
- 🔁 New sessions repeat mistakes from yesterday  
- 📂 HANDOFF notes, devlogs, and error logs are scattered everywhere
- 🤔 You don't know which agent to trust for which task

**Conductor** brings order to this chaos.

## What's Inside

### 📖 Methodology — The 12 Dimensions of Human-Agent Interaction

We identified 12 dimensions that matter when a human works with multiple AI agents:

| # | Dimension | What It Covers |
|---|-----------|---------------|
| 1 | **Handoff Management** | Passing context between sessions without loss |
| 2 | **Knowledge Capture** | Recording decisions, errors, and QA pairs |
| 3 | **Trust Calibration** | Knowing when to verify vs. trust the agent |
| 4 | **Cognitive Load** | Managing your mental bandwidth across agents |
| 5 | **Prompt Quality** | Improving how you communicate with agents |
| 6 | **Agent Profiling** | Tracking each agent's strengths and weaknesses |
| 7 | **Tool Selection** | Picking the right agent for the right task |
| 8 | **Feedback Loops** | Turning errors into prevention rules |
| 9 | **Attention Allocation** | Deciding which project needs you right now |
| 10 | **Disagreement Resolution** | Handling conflicting agent advice |
| 11 | **Cross-Agent Consistency** | Keeping agents aligned on decisions |
| 12 | **Energy Modeling** | Adjusting oversight based on your fatigue |

Read more: [docs/](docs/)

### 📁 Templates — Copy, paste, done

| Template | Purpose |
|----------|---------|
| [`HANDOFF.md`](templates/HANDOFF.md.template) | Session-end context handoff |
| [`CLAUDE.md`](templates/CLAUDE.md.template) | Agent rules with handoff protocol |
| [`ERROR_BOOK.md`](templates/ERROR_BOOK.md.template) | AI mistake tracker for trust calibration |
| [`TRUST_PROFILE.md`](templates/TRUST_PROFILE.md.template) | Agent reliability scorecard |

### 🧰 CLI — See all your projects at a glance

```bash
$ conductor status

🎵 Conductor · Project Status
┌─────────────┬────────────┬────────┬──────────────────────┐
│ Project     │ Last Active│ Status │ Next Step            │
├─────────────┼────────────┼────────┼──────────────────────┤
│ wenyuan     │ 6h ago     │ ✅     │ Refactor README      │
│ network-opt │ 2h ago     │ ✅     │ VPS setup            │
│ conductor   │ 30m ago    │ ✅     │ Write tests          │
│ old-project │ 3d ago     │ 🔴     │ Archive or continue? │
└─────────────┴────────────┴────────┴──────────────────────┘
 📅 2026-04-09 │ 4 projects │ 5 decisions │ 12 files Δ
```

## Quick Start

### Option A: Just use the templates (no install needed)

1. Copy [`templates/HANDOFF.md.template`](templates/HANDOFF.md.template) to your project as `HANDOFF.md`
2. Copy the handoff protocol from [`templates/CLAUDE.md.template`](templates/CLAUDE.md.template) into your project's `CLAUDE.md`
3. Tell your AI: *"Read HANDOFF.md before starting. Update it before ending."*

### Option B: Install the CLI

```bash
pip install conductor-ai
conductor init ./my-project
conductor status
```

## Core Concepts

### The Handoff Protocol

Every session ends with a structured handoff:

```markdown
## 2026-04-09
- done: Implemented user auth module
- decisions: Chose JWT over sessions (stateless, scales better)
- pitfall: bcrypt 5.x changed default rounds — broke existing hashes
- next: Add password reset flow
```

**500 token max.** If you can't summarize it, you don't understand it.

→ [Full protocol](docs/handoff-protocol.md)

### Trust Calibration

Don't blindly trust or distrust your AI. Calibrate per domain:

| Layer | Method |
|-------|--------|
| L1 | **Verify outcomes** — does the code run? |
| L2 | **Cross-verify** — have another agent review |
| L3 | **Progressive trust** — try on one file first |
| L4 | **Demand explanation** — ask WHY, not just WHAT |

→ [Full framework](docs/trust-calibration.md)

### Task Sizing (S/M/L)

Not every task needs a full planning cycle:

| Size | Time | Process |
|------|------|---------|
| **S** | < 30min | Just do it → test → commit → HANDOFF |
| **M** | 1-3h | Brief plan → execute → HANDOFF |
| **L** | > 3h | Brainstorm → plan → TDD → review → HANDOFF |

→ [Full guide](docs/task-sizing.md)

## Why Conductor?

| vs. | Difference |
|-----|-----------|
| **CrewAI / LangGraph** | They orchestrate agent-to-agent. We orchestrate **human-to-agents**. |
| **OpenSpec** | OpenSpec manages specs within one session. We manage **across sessions and agents**. |
| **CLAUDE.md alone** | CLAUDE.md is one file. We're a **complete methodology + tools**. |
| **Nothing** | You're losing decisions, repeating mistakes, and burning context window tokens. |

## Roadmap

- [x] v0.1 — Methodology docs + templates + `conductor status`
- [ ] v0.2 — `conductor digest` — extract decisions/errors from conversation logs
- [ ] v0.3 — Agent Retrospective — structured post-session review
- [ ] v0.4 — Memory system — persistent cross-session knowledge store

## Philosophy

> *"If you just drive the AI to work and walk away, you'll never know what you don't know. The original sin of AI-assisted development is not reviewing, not reflecting, not improving."*

Conductor is built on three principles:

1. **Structure over ceremony** — Lightweight protocols that actually get followed, not heavy processes that get skipped.
2. **Observe, then trust** — Build trust through data (error books, trust profiles), not assumptions.
3. **The human improves too** — It's not just about making AI better. It's about making *you* better at working with AI.

## Contributing

Contributions welcome! Please read the methodology docs first to understand the philosophy.

## License

[MIT](LICENSE)
