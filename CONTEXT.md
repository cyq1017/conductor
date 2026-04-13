# CONTEXT.md — Conductor

## What is this project?
Conductor is a CLI tool for orchestrating multiple AI coding agents (Claude Code, Cursor, Copilot, Codex, Antigravity, etc.) with structured handoffs, trust calibration, and continuous improvement.

## Tech Stack
- **Language**: Python 3.9+
- **CLI Framework**: Click
- **Output**: Rich (tables, panels, styled text)
- **Data**: JSON files (memory store), Markdown files (HANDOFF, ERROR_BOOK)
- **Packaging**: setuptools, published on PyPI as `conductor-ai`
- **Testing**: pytest

## Project Structure
```
conductor/
├── src/conductor/
│   ├── cli.py          # Main CLI entry point (Click commands)
│   ├── status.py       # `conductor status` — multi-project dashboard
│   ├── digest.py       # `conductor digest` — extract decisions from logs
│   ├── retro.py        # `conductor retro` — interactive retrospective
│   ├── memory.py       # `conductor memory` — cross-session knowledge store
│   └── init.py         # `conductor init` — scaffold project files
├── templates/          # HANDOFF.md, ERROR_BOOK.md, TRUST_PROFILE.md templates
├── docs/
│   ├── methodology/    # 3 methodology articles
│   ├── ERROR_BOOK.md   # Project's own error tracking
│   ├── TRUST_PROFILE.md
│   └── retro_log.jsonl
├── README.md           # English
├── README_zh.md        # Chinese
└── pyproject.toml      # Package config
```

## Key Design Decisions
- **File-based memory over database**: Zero dependencies, human-readable, git-trackable
- **CLI over web UI**: Agents work in terminals, so the tool should too
- **Agent-agnostic**: Works with any AI coding tool, not tied to one vendor
- **Methodology-first**: The ideas (HANDOFF protocol, trust calibration) are more valuable than the code

## Commands
| Command | Purpose |
|---------|---------|
| `conductor status [path]` | Show project health dashboard |
| `conductor init [path]` | Scaffold HANDOFF.md + ERROR_BOOK.md + TRUST_PROFILE.md |
| `conductor digest [path]` | Extract decisions and errors from project history |
| `conductor retro [path]` | Run interactive agent retrospective |
| `conductor memory set/get/list` | Cross-session key-value knowledge store |

## Current Version
v0.4.0 — All 5 commands implemented, published on PyPI.

## Things to Watch Out For
- The `retro` command is interactive (stdin prompts) — don't try to automate it without handling prompts
- Memory store is a flat JSON file at `.conductor/memory.json` — not designed for concurrent writes
- Templates in `templates/` are meant to be copied, not imported as Python modules
