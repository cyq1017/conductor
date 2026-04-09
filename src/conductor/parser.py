"""Parse HANDOFF.md files and git status for project information."""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


@dataclass
class ProjectStatus:
    """Status information for a single project."""

    name: str
    path: Path
    last_updated: Optional[datetime] = None
    last_commit_time: Optional[datetime] = None
    last_commit_msg: str = ""
    files_changed_today: int = 0
    next_steps: list[str] = field(default_factory=list)
    decisions: list[str] = field(default_factory=list)
    blocked: list[str] = field(default_factory=list)
    has_handoff: bool = True


def parse_project_status(project_path: Path) -> ProjectStatus:
    """Parse HANDOFF.md and git info to build a ProjectStatus.

    Args:
        project_path: Path to the project root directory.

    Returns:
        ProjectStatus with parsed information.
    """
    status = ProjectStatus(name=project_path.name, path=project_path)

    # Parse HANDOFF.md
    handoff_path = project_path / "HANDOFF.md"
    if handoff_path.exists():
        _parse_handoff(handoff_path, status)

    # Parse git info
    _parse_git_info(project_path, status)

    return status


def _parse_handoff(handoff_path: Path, status: ProjectStatus) -> None:
    """Extract key information from HANDOFF.md."""
    try:
        content = handoff_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return

    # Extract date from ## YYYY-MM-DD pattern
    date_match = re.search(r"##\s+(\d{4}-\d{2}-\d{2})", content)
    if date_match:
        try:
            status.last_updated = datetime.strptime(
                date_match.group(1), "%Y-%m-%d"
            ).replace(tzinfo=timezone.utc)
        except ValueError:
            pass

    # Fall back to file modification time
    if status.last_updated is None:
        mtime = handoff_path.stat().st_mtime
        status.last_updated = datetime.fromtimestamp(mtime, tz=timezone.utc)

    # Extract next steps
    next_section = re.search(
        r"###?\s*(?:Next Steps?|next)\s*\n(.*?)(?=\n###?\s|\n---|\Z)",
        content,
        re.DOTALL | re.IGNORECASE,
    )
    if next_section:
        lines = next_section.group(1).strip().split("\n")
        status.next_steps = [
            re.sub(r"^[\s\-\d.]+", "", line).strip()
            for line in lines
            if line.strip() and not line.strip().startswith("#")
        ][:3]  # Max 3 items

    # Extract blocked items
    blocked_section = re.search(
        r"###?\s*(?:Blocked|blocked)\s*\n(.*?)(?=\n###?\s|\n---|\Z)",
        content,
        re.DOTALL | re.IGNORECASE,
    )
    if blocked_section:
        text = blocked_section.group(1).strip()
        if text and "skip" not in text.lower() and "none" not in text.lower():
            lines = text.split("\n")
            status.blocked = [
                re.sub(r"^[\s\-]+", "", line).strip()
                for line in lines
                if line.strip() and not line.strip().startswith("#")
            ]

    # Extract decisions
    decisions_section = re.search(
        r"###?\s*(?:Decisions?|decisions?)\s*\n(.*?)(?=\n###?\s|\n---|\Z)",
        content,
        re.DOTALL | re.IGNORECASE,
    )
    if decisions_section:
        lines = decisions_section.group(1).strip().split("\n")
        status.decisions = [
            re.sub(r"^[\s\-]+", "", line).strip()
            for line in lines
            if line.strip() and not line.strip().startswith("#")
        ]


def _parse_git_info(project_path: Path, status: ProjectStatus) -> None:
    """Extract git information for the project."""
    git_dir = project_path / ".git"
    if not git_dir.exists():
        return

    # Last commit time and message
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%aI|%s"],
            capture_output=True,
            text=True,
            cwd=project_path,
            timeout=5,
        )
        if result.returncode == 0 and result.stdout.strip():
            parts = result.stdout.strip().split("|", 1)
            if len(parts) == 2:
                try:
                    status.last_commit_time = datetime.fromisoformat(parts[0])
                except ValueError:
                    pass
                status.last_commit_msg = parts[1][:60]  # Truncate long messages
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    # Files changed today
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        result = subprocess.run(
            ["git", "log", "--since", f"{today}T00:00:00", "--format=", "--numstat"],
            capture_output=True,
            text=True,
            cwd=project_path,
            timeout=5,
        )
        if result.returncode == 0:
            # Count unique files changed
            files = set()
            for line in result.stdout.strip().split("\n"):
                parts = line.split("\t")
                if len(parts) == 3:
                    files.add(parts[2])
            status.files_changed_today = len(files)
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
