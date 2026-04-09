"""Rich TUI rendering for digest output."""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from conductor.digest import ProjectDigest


def render_digest(digest: ProjectDigest) -> None:
    """Render a project digest with Rich TUI."""
    console = Console()

    # Header
    console.print()
    title = Text("🎵 Conductor · Project Digest", style="bold cyan")
    console.print(Panel(title, border_style="cyan", expand=False))
    console.print(
        f"  📁 {digest.project_name}  │  "
        f"📅 {digest.date_range or 'No dates'}  │  "
        f"🔄 {digest.sessions_count} sessions"
    )
    console.print()

    # Decisions
    if digest.decisions:
        table = Table(
            title="📋 Decisions Made",
            show_header=True,
            header_style="bold green",
            border_style="green",
            expand=True,
        )
        table.add_column("Date", style="dim", width=12)
        table.add_column("Decision", ratio=1)
        table.add_column("Source", style="dim", width=14)

        for entry in digest.decisions:
            table.add_row(
                entry.date or "—",
                entry.content,
                entry.source_file,
            )
        console.print(table)
        console.print()

    # Errors & Pitfalls
    if digest.errors:
        table = Table(
            title="⚠️  Errors & Pitfalls",
            show_header=True,
            header_style="bold red",
            border_style="red",
            expand=True,
        )
        table.add_column("Date", style="dim", width=12)
        table.add_column("Issue", ratio=1)
        table.add_column("Source", style="dim", width=14)

        for entry in digest.errors:
            table.add_row(
                entry.date or "—",
                entry.content,
                entry.source_file,
            )
        console.print(table)
        console.print()

    # Completed Items
    if digest.completed:
        table = Table(
            title="✅ Completed",
            show_header=True,
            header_style="bold blue",
            border_style="blue",
            expand=True,
        )
        table.add_column("Date", style="dim", width=12)
        table.add_column("What Was Done", ratio=1)

        for entry in digest.completed:
            table.add_row(entry.date or "—", entry.content)
        console.print(table)
        console.print()

    # Next Steps (only show from latest session)
    if digest.next_steps:
        latest_next = [
            e for e in digest.next_steps
            if e.date == max(n.date for n in digest.next_steps if n.date)
        ] if any(n.date for n in digest.next_steps) else digest.next_steps

        console.print("📌 [bold yellow]Outstanding Next Steps[/]")
        for entry in latest_next:
            console.print(f"   → {entry.content}")
        console.print()

    # Summary stats
    console.print(
        f"  ─── 📊 {len(digest.decisions)} decisions │ "
        f"{len(digest.errors)} errors │ "
        f"{len(digest.completed)} completed │ "
        f"{len(digest.next_steps)} next steps ───"
    )
    console.print()
