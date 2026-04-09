"""Agent Retrospective — structured post-session review.

Guides the user through evaluating their AI agent's performance,
then updates ERROR_BOOK.md and TRUST_PROFILE.md automatically.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional


# Trust domains for profiling
TRUST_DOMAINS = [
    "code_generation",
    "debugging",
    "architecture",
    "testing",
    "documentation",
    "refactoring",
    "devops",
    "ui_frontend",
]

TRUST_DOMAIN_LABELS = {
    "code_generation": "Code Generation",
    "debugging": "Debugging",
    "architecture": "Architecture & Design",
    "testing": "Testing",
    "documentation": "Documentation",
    "refactoring": "Refactoring",
    "devops": "DevOps / CI/CD",
    "ui_frontend": "UI / Frontend",
}


@dataclass
class RetroEntry:
    """A single retrospective entry."""

    date: str
    agent_name: str
    project: str

    # What happened
    task_description: str = ""
    task_size: str = ""  # S / M / L

    # Evaluation
    went_well: list[str] = field(default_factory=list)
    went_wrong: list[str] = field(default_factory=list)
    surprises: list[str] = field(default_factory=list)

    # Trust adjustments
    trust_adjustments: dict[str, int] = field(default_factory=dict)
    # +1 = performed better than expected
    #  0 = as expected
    # -1 = performed worse than expected

    # Errors to log
    errors: list[dict] = field(default_factory=list)
    # Each error: {"description": str, "root_cause": str, "prevention": str}

    # Action items
    new_rules: list[str] = field(default_factory=list)  # Rules to add to CLAUDE.md


def run_interactive_retro(project_path: Path) -> Optional[RetroEntry]:
    """Run an interactive retrospective session.

    Returns:
        RetroEntry with collected data, or None if user cancels.
    """
    from rich.console import Console
    from rich.prompt import Prompt, IntPrompt, Confirm
    from rich.panel import Panel
    from rich.text import Text

    console = Console()
    console.print()
    console.print(Panel(
        Text("🎵 Conductor · Agent Retrospective", style="bold cyan"),
        border_style="cyan",
        expand=False,
    ))
    console.print()

    today = datetime.now().strftime("%Y-%m-%d")

    # Basic info
    agent_name = Prompt.ask(
        "🤖 Which agent did you use?",
        default="claude-code",
        choices=["claude-code", "cursor", "codex", "antigravity", "gemini-cli",
                 "kimi-code", "windsurf", "copilot", "aider", "other"],
    )
    task_desc = Prompt.ask("📝 Brief description of the task")
    task_size = Prompt.ask(
        "📏 Task size",
        choices=["S", "M", "L"],
        default="M",
    )

    entry = RetroEntry(
        date=today,
        agent_name=agent_name,
        project=project_path.name,
        task_description=task_desc,
        task_size=task_size,
    )

    # What went well
    console.print("\n[bold green]✅ What went well?[/] (enter empty line to stop)")
    while True:
        item = Prompt.ask("  +", default="")
        if not item:
            break
        entry.went_well.append(item)

    # What went wrong
    console.print("\n[bold red]❌ What went wrong?[/] (enter empty line to stop)")
    while True:
        item = Prompt.ask("  -", default="")
        if not item:
            break
        entry.went_wrong.append(item)

    # Errors to log
    if entry.went_wrong:
        console.print(
            "\n[bold yellow]📋 Log any errors for the Error Book?[/]"
        )
        while True:
            if not Confirm.ask("  Add an error?", default=len(entry.errors) == 0):
                break
            desc = Prompt.ask("  Description")
            root = Prompt.ask("  Root cause", default="Unknown")
            prevention = Prompt.ask("  How to prevent next time", default="")
            entry.errors.append({
                "description": desc,
                "root_cause": root,
                "prevention": prevention,
            })

    # Trust adjustments
    console.print(
        "\n[bold cyan]🎯 Trust calibration[/] "
        "(rate agent in domains it worked on: -1 worse / 0 expected / +1 better)"
    )
    console.print("  [dim]Skip domains the agent didn't touch[/]")

    for domain in TRUST_DOMAINS:
        label = TRUST_DOMAIN_LABELS[domain]
        try:
            score = IntPrompt.ask(
                f"  {label}",
                default=None,
                choices=["-1", "0", "1"],
            )
            entry.trust_adjustments[domain] = score
        except (KeyboardInterrupt, EOFError):
            break

    # New rules
    console.print(
        "\n[bold magenta]📜 New rules for CLAUDE.md?[/] "
        "(enter empty to stop)"
    )
    while True:
        rule = Prompt.ask("  Rule", default="")
        if not rule:
            break
        entry.new_rules.append(rule)

    return entry


def save_retro(entry: RetroEntry, project_path: Path) -> dict[str, bool]:
    """Save retrospective results to project files.

    Updates:
    - docs/ERROR_BOOK.md — append new errors
    - docs/TRUST_PROFILE.md — update trust scores
    - docs/retro_log.jsonl — append raw retro data

    Returns:
        Dict of which files were updated.
    """
    results = {}

    # Save to retro log (raw data)
    retro_log = project_path / "docs" / "retro_log.jsonl"
    retro_log.parent.mkdir(parents=True, exist_ok=True)
    with open(retro_log, "a", encoding="utf-8") as f:
        data = {
            "date": entry.date,
            "agent": entry.agent_name,
            "project": entry.project,
            "task": entry.task_description,
            "size": entry.task_size,
            "went_well": entry.went_well,
            "went_wrong": entry.went_wrong,
            "errors": entry.errors,
            "trust": entry.trust_adjustments,
            "new_rules": entry.new_rules,
        }
        f.write(json.dumps(data, ensure_ascii=False) + "\n")
    results["retro_log.jsonl"] = True

    # Update ERROR_BOOK.md
    if entry.errors:
        error_book = project_path / "docs" / "ERROR_BOOK.md"
        _append_errors(error_book, entry)
        results["ERROR_BOOK.md"] = True

    # Update TRUST_PROFILE.md
    if entry.trust_adjustments:
        trust_profile = project_path / "docs" / "TRUST_PROFILE.md"
        _update_trust_profile(trust_profile, entry)
        results["TRUST_PROFILE.md"] = True

    return results


def _append_errors(error_book_path: Path, entry: RetroEntry) -> None:
    """Append errors to ERROR_BOOK.md."""
    if not error_book_path.exists():
        error_book_path.write_text(
            "# AI Error Book\n\n"
            "> Track AI mistakes for trust calibration.\n"
            "> Updated by `conductor retro`.\n\n"
        )

    content = error_book_path.read_text(encoding="utf-8")

    new_entries = []
    for error in entry.errors:
        new_entries.append(
            f"\n## {entry.date} — {entry.agent_name}\n\n"
            f"**Task**: {entry.task_description}\n\n"
            f"**Error**: {error['description']}\n\n"
            f"**Root Cause**: {error['root_cause']}\n\n"
            f"**Prevention**: {error['prevention']}\n"
        )

    content += "\n".join(new_entries)
    error_book_path.write_text(content, encoding="utf-8")


def _update_trust_profile(trust_path: Path, entry: RetroEntry) -> None:
    """Update or create TRUST_PROFILE.md with trust adjustments."""

    # Load existing scores or start fresh
    scores = _load_trust_scores(trust_path)

    # Apply adjustments
    for domain, adjustment in entry.trust_adjustments.items():
        if domain not in scores:
            scores[domain] = {"score": 50, "samples": 0}  # Start at 50/100
        current = scores[domain]["score"]
        # Weighted update: each retro moves the score by up to 5 points
        delta = adjustment * 5
        scores[domain]["score"] = max(0, min(100, current + delta))
        scores[domain]["samples"] += 1

    # Write updated profile
    _write_trust_profile(trust_path, entry.agent_name, scores)


def _load_trust_scores(trust_path: Path) -> dict:
    """Load existing trust scores from TRUST_PROFILE.md."""
    scores = {}

    if not trust_path.exists():
        return scores

    import re
    content = trust_path.read_text(encoding="utf-8")

    # Parse score lines like: | Code Generation | 65 | 3 |
    for match in re.finditer(
        r"\|\s*(\w[\w\s/&]+\w)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|", content
    ):
        label = match.group(1).strip()
        score = int(match.group(2))
        samples = int(match.group(3))

        # Map label back to domain key
        for key, lab in TRUST_DOMAIN_LABELS.items():
            if lab == label:
                scores[key] = {"score": score, "samples": samples}
                break

    return scores


def _write_trust_profile(
    trust_path: Path, agent_name: str, scores: dict
) -> None:
    """Write trust profile markdown."""
    lines = [
        "# Agent Trust Profile\n",
        f"\n> Agent: **{agent_name}**\n",
        f"> Last updated: {datetime.now().strftime('%Y-%m-%d')}\n",
        "> Updated by `conductor retro`.\n",
        "\n## Trust Scores\n",
        "\n| Domain | Score (0-100) | Samples |",
        "\n|--------|--------------|---------|",
    ]

    for domain in TRUST_DOMAINS:
        label = TRUST_DOMAIN_LABELS[domain]
        if domain in scores:
            score = scores[domain]["score"]
            samples = scores[domain]["samples"]
            # Add visual bar
            bar_len = score // 10
            bar = "█" * bar_len + "░" * (10 - bar_len)
            lines.append(f"\n| {label} | {bar} {score} | {samples} |")

    lines.append(
        "\n\n## Score Guide\n"
        "\n- **80-100**: High trust — minimal review needed\n"
        "- **60-79**: Moderate trust — spot-check results\n"
        "- **40-59**: Low trust — review everything\n"
        "- **0-39**: Very low trust — consider different agent for this domain\n"
    )

    trust_path.write_text("".join(lines), encoding="utf-8")
