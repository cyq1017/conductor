"""Digest engine — extract decisions, errors, and patterns from project files.

Scans HANDOFF.md, ERROR_BOOK.md, and conversation logs to produce
a structured digest of what happened across sessions.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class DigestEntry:
    """A single extracted item from project history."""

    type: str  # "decision", "error", "pitfall", "next", "done"
    content: str
    date: Optional[str] = None
    source_file: str = ""


@dataclass
class ProjectDigest:
    """Aggregated digest for a project."""

    project_name: str
    project_path: Path
    entries: list[DigestEntry] = field(default_factory=list)
    sessions_count: int = 0
    date_range: str = ""

    @property
    def decisions(self) -> list[DigestEntry]:
        return [e for e in self.entries if e.type == "decision"]

    @property
    def errors(self) -> list[DigestEntry]:
        return [e for e in self.entries if e.type in ("error", "pitfall")]

    @property
    def completed(self) -> list[DigestEntry]:
        return [e for e in self.entries if e.type == "done"]

    @property
    def next_steps(self) -> list[DigestEntry]:
        return [e for e in self.entries if e.type == "next"]


def digest_project(project_path: Path) -> ProjectDigest:
    """Extract a full digest from a project's Conductor files.

    Scans:
    - HANDOFF.md — session records
    - docs/ERROR_BOOK.md — error history
    - docs/devlog.md — development log (if exists)

    Args:
        project_path: Path to project root.

    Returns:
        ProjectDigest with all extracted entries.
    """
    digest = ProjectDigest(
        project_name=project_path.name,
        project_path=project_path,
    )

    # Parse HANDOFF.md
    handoff_path = project_path / "HANDOFF.md"
    if handoff_path.exists():
        _digest_handoff(handoff_path, digest)

    # Parse ERROR_BOOK.md
    error_book = project_path / "docs" / "ERROR_BOOK.md"
    if error_book.exists():
        _digest_error_book(error_book, digest)

    # Parse devlog.md
    devlog = project_path / "docs" / "devlog.md"
    if devlog.exists():
        _digest_devlog(devlog, digest)

    # Compute date range
    dates = [e.date for e in digest.entries if e.date]
    if dates:
        digest.date_range = f"{min(dates)} → {max(dates)}"

    return digest


def _digest_handoff(handoff_path: Path, digest: ProjectDigest) -> None:
    """Extract entries from HANDOFF.md."""
    try:
        content = handoff_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return

    # Split into sessions by date headers
    sessions = re.split(r"(?=##\s+\d{4}-\d{2}-\d{2})", content)

    for session in sessions:
        date_match = re.search(r"##\s+(\d{4}-\d{2}-\d{2})", session)
        if not date_match:
            continue

        date = date_match.group(1)
        digest.sessions_count += 1

        # Extract done items
        _extract_list_items(
            session, r"(?:done|completed|Done|Completed)", date,
            "done", "HANDOFF.md", digest,
        )

        # Extract decisions
        _extract_list_items(
            session, r"(?:decisions?|Decisions?)", date,
            "decision", "HANDOFF.md", digest,
        )

        # Extract pitfalls
        _extract_list_items(
            session, r"(?:pitfalls?|Pitfalls?)", date,
            "pitfall", "HANDOFF.md", digest,
        )

        # Extract next steps
        _extract_list_items(
            session, r"(?:next|Next)", date,
            "next", "HANDOFF.md", digest,
        )

        # Extract blocked items
        _extract_list_items(
            session, r"(?:blocked|Blocked)", date,
            "blocked", "HANDOFF.md", digest,
        )


def _extract_list_items(
    text: str,
    key_pattern: str,
    date: str,
    entry_type: str,
    source: str,
    digest: ProjectDigest,
) -> None:
    """Extract bullet-point items after a key like 'done:', 'decisions:', etc."""
    # Pattern 1: key: value (inline format)
    inline_pattern = rf"-\s*{key_pattern}\s*:\s*(.+)"
    for match in re.finditer(inline_pattern, text):
        content = match.group(1).strip()
        if content and content.lower() not in ("none", "n/a", "skip"):
            digest.entries.append(
                DigestEntry(
                    type=entry_type,
                    content=content,
                    date=date,
                    source_file=source,
                )
            )

    # Pattern 2: ### Key\n- item1\n- item2 (section format)
    section_pattern = rf"###?\s*{key_pattern}\s*\n((?:\s*[-*]\s+.+\n?)+)"
    section_match = re.search(section_pattern, text, re.IGNORECASE)
    if section_match:
        lines = section_match.group(1).strip().split("\n")
        for line in lines:
            content = re.sub(r"^\s*[-*]\s+", "", line).strip()
            if content and content.lower() not in ("none", "n/a", "skip"):
                digest.entries.append(
                    DigestEntry(
                        type=entry_type,
                        content=content,
                        date=date,
                        source_file=source,
                    )
                )


def _digest_error_book(error_book_path: Path, digest: ProjectDigest) -> None:
    """Extract entries from ERROR_BOOK.md."""
    try:
        content = error_book_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return

    # Extract error entries (## date or ### Error: description patterns)
    error_blocks = re.split(r"(?=##\s+)", content)
    for block in error_blocks:
        if not block.strip():
            continue

        date_match = re.search(r"(\d{4}-\d{2}-\d{2})", block)
        date = date_match.group(1) if date_match else None

        # Extract the error description
        header_match = re.search(r"##\s+(.+)", block)
        if header_match:
            header = header_match.group(1).strip()
            # Skip the main title
            if header.lower() in ("ai error book", "error book", "errors"):
                continue

            # Look for description in the body
            body_lines = []
            for line in block.split("\n")[1:]:
                line = line.strip()
                if line and not line.startswith("#"):
                    body_lines.append(line)

            description = header
            if body_lines:
                # Use first meaningful line as description
                first_line = re.sub(r"^[-*>\s]+", "", body_lines[0]).strip()
                if first_line:
                    description = f"{header}: {first_line}"

            digest.entries.append(
                DigestEntry(
                    type="error",
                    content=description,
                    date=date,
                    source_file="ERROR_BOOK.md",
                )
            )


def _digest_devlog(devlog_path: Path, digest: ProjectDigest) -> None:
    """Extract key items from devlog.md."""
    try:
        content = devlog_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return

    # Extract date-headed sections
    sections = re.split(r"(?=##\s+\d{4}-\d{2}-\d{2})", content)
    for section in sections:
        date_match = re.search(r"##\s+(\d{4}-\d{2}-\d{2})", section)
        if not date_match:
            continue
        date = date_match.group(1)

        # Extract decisions from devlog
        _extract_list_items(
            section, r"(?:decisions?|Decisions?|chose|selected)",
            date, "decision", "devlog.md", digest,
        )
