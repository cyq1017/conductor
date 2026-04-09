"""Rich TUI display for Conductor status output."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import List

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from conductor.parser import ProjectStatus


def _format_time_ago(dt: datetime | None) -> str:
    """Format a datetime as a human-readable 'X ago' string."""
    if dt is None:
        return "unknown"

    now = datetime.now(tz=timezone.utc)

    # Ensure dt is timezone-aware
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    delta = now - dt
    total_seconds = int(delta.total_seconds())

    if total_seconds < 0:
        return "just now"
    elif total_seconds < 60:
        return f"{total_seconds}s ago"
    elif total_seconds < 3600:
        minutes = total_seconds // 60
        return f"{minutes}m ago"
    elif total_seconds < 86400:
        hours = total_seconds // 3600
        return f"{hours}h ago"
    else:
        days = total_seconds // 86400
        return f"{days}d ago"


def _freshness_icon(dt: datetime | None, stale_hours: int) -> str:
    """Return an icon based on how recently the project was updated."""
    if dt is None:
        return "❓"

    now = datetime.now(tz=timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    hours = (now - dt).total_seconds() / 3600

    if hours < stale_hours:
        return "✅"
    elif hours < stale_hours * 2:
        return "⚠️"
    else:
        return "🔴"


def render_status_table(
    statuses: List[ProjectStatus], stale_hours: int = 12
) -> None:
    """Render a rich table showing all project statuses.

    Args:
        statuses: List of ProjectStatus objects to display.
        stale_hours: Number of hours before marking a project as stale.
    """
    console = Console()

    # Header
    console.print()

    # Main status table
    table = Table(
        title="🎵 Conductor · Project Status",
        title_style="bold cyan",
        border_style="bright_black",
        show_lines=True,
        padding=(0, 1),
    )
    table.add_column("Project", style="bold white", min_width=15)
    table.add_column("Last Active", justify="right", min_width=10)
    table.add_column("Status", justify="center", min_width=6)
    table.add_column("Next Step", style="dim", max_width=40)

    # Sort by last_updated (most recent first), None values last
    sorted_statuses = sorted(
        statuses,
        key=lambda s: s.last_updated or datetime.min.replace(tzinfo=timezone.utc),
        reverse=True,
    )

    total_decisions = 0
    total_files = 0
    total_blocked = 0

    for s in sorted_statuses:
        # Determine most recent activity time
        active_time = s.last_updated
        if s.last_commit_time:
            if active_time is None or (
                s.last_commit_time.replace(tzinfo=timezone.utc)
                if s.last_commit_time.tzinfo is None
                else s.last_commit_time
            ) > (
                active_time.replace(tzinfo=timezone.utc)
                if active_time.tzinfo is None
                else active_time
            ):
                active_time = s.last_commit_time

        time_ago = _format_time_ago(active_time)
        icon = _freshness_icon(active_time, stale_hours)

        # Format next step
        next_step = s.next_steps[0] if s.next_steps else ""
        if len(next_step) > 40:
            next_step = next_step[:37] + "..."

        # Blocked indicator
        if s.blocked:
            icon = "🚫"
            next_step = f"BLOCKED: {s.blocked[0][:30]}"

        table.add_row(s.name, time_ago, icon, next_step)

        total_decisions += len(s.decisions)
        total_files += s.files_changed_today
        total_blocked += len(s.blocked)

    console.print(table)

    # Summary line
    today = datetime.now().strftime("%Y-%m-%d")
    summary_parts = [
        f"📅 {today}",
        f"{len(statuses)} projects",
        f"{total_decisions} decisions",
        f"{total_files} files Δ",
    ]
    if total_blocked > 0:
        summary_parts.append(f"🚫 {total_blocked} blocked")

    summary = Text(" │ ".join(summary_parts), style="dim")
    console.print(Panel(summary, border_style="bright_black", padding=(0, 1)))
    console.print()
