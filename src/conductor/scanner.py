"""Scan directories for projects that have HANDOFF.md files."""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional


def scan_projects(
    scan_dir: str, exclude: Optional[List[str]] = None
) -> List[Path]:
    """Scan a directory for subdirectories containing HANDOFF.md.

    Args:
        scan_dir: Root directory to scan (e.g., "~/projects")
        exclude: Directory names to skip (e.g., ["archive", ".git"])

    Returns:
        List of project paths that contain a HANDOFF.md file.
    """
    if exclude is None:
        exclude = ["archive", ".git", "node_modules", "__pycache__", ".venv", "venv"]

    root = Path(scan_dir).expanduser().resolve()

    if not root.exists():
        return []

    projects = []

    for child in sorted(root.iterdir()):
        if not child.is_dir():
            continue

        if child.name.startswith(".") or child.name in exclude:
            continue

        handoff = child / "HANDOFF.md"
        if handoff.exists():
            projects.append(child)

    return projects
