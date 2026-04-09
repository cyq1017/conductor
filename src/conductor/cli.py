"""CLI entry point for Conductor."""

import click

from conductor.scanner import scan_projects
from conductor.parser import parse_project_status
from conductor.display import render_status_table


from conductor import __version__


@click.group()
@click.version_option(version=__version__, prog_name="conductor")
def main():
    """Conductor — Orchestrate multiple AI coding agents.

    Structured handoff. Trust calibration. Continuous improvement.
    """
    pass


@main.command()
@click.option(
    "--dir",
    "-d",
    "scan_dir",
    default="~/projects",
    help="Directory to scan for projects (default: ~/projects)",
)
@click.option(
    "--stale",
    "-s",
    "stale_hours",
    default=12,
    type=int,
    help="Hours before a project is marked stale (default: 12)",
)
def status(scan_dir: str, stale_hours: int):
    """Show status of all projects with HANDOFF.md files."""
    projects = scan_projects(scan_dir)

    if not projects:
        click.echo(f"No projects with HANDOFF.md found in {scan_dir}")
        click.echo("Run 'conductor init <project-path>' to set up a project.")
        return

    statuses = []
    for project_path in projects:
        project_status = parse_project_status(project_path)
        statuses.append(project_status)

    render_status_table(statuses, stale_hours=stale_hours)


@main.command()
@click.argument("project_path", default=".")
@click.option(
    "--json",
    "output_json",
    is_flag=True,
    default=False,
    help="Output as JSON instead of TUI",
)
def digest(project_path: str, output_json: bool):
    """Extract decisions, errors, and patterns from a project.

    Scans HANDOFF.md, ERROR_BOOK.md, and devlog.md to produce
    a structured summary of what happened across sessions.
    """
    import json
    from pathlib import Path
    from conductor.digest import digest_project
    from conductor.digest_display import render_digest

    project = Path(project_path).expanduser().resolve()

    if not project.exists():
        click.echo(f"Error: {project} does not exist.")
        return

    handoff = project / "HANDOFF.md"
    if not handoff.exists():
        click.echo(f"No HANDOFF.md found in {project.name}")
        click.echo("Run 'conductor init' first.")
        return

    result = digest_project(project)

    if output_json:
        data = {
            "project": result.project_name,
            "sessions": result.sessions_count,
            "date_range": result.date_range,
            "decisions": [
                {"date": e.date, "content": e.content, "source": e.source_file}
                for e in result.decisions
            ],
            "errors": [
                {"date": e.date, "content": e.content, "source": e.source_file}
                for e in result.errors
            ],
            "completed": [
                {"date": e.date, "content": e.content}
                for e in result.completed
            ],
            "next_steps": [
                {"date": e.date, "content": e.content}
                for e in result.next_steps
            ],
        }
        click.echo(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        render_digest(result)


@main.command()
@click.argument("project_path", default=".")
def retro(project_path: str):
    """Run an interactive Agent Retrospective.

    Guides you through evaluating your AI agent's performance,
    then automatically updates ERROR_BOOK.md and TRUST_PROFILE.md.
    """
    from pathlib import Path
    from conductor.retro import run_interactive_retro, save_retro

    project = Path(project_path).expanduser().resolve()

    if not project.exists():
        click.echo(f"Error: {project} does not exist.")
        return

    entry = run_interactive_retro(project)

    if entry is None:
        click.echo("Retro cancelled.")
        return

    results = save_retro(entry, project)

    click.echo()
    for filename, success in results.items():
        if success:
            click.echo(f"  ✅ Updated docs/{filename}")

    click.echo(f"\n🎵 Retrospective saved for {project.name}!")

    if entry.new_rules:
        click.echo("\n📜 Don't forget to add these rules to your CLAUDE.md:")
        for rule in entry.new_rules:
            click.echo(f"   → {rule}")


@main.group()
def memory():
    """Manage project memory — persistent cross-session knowledge.

    Store facts, decisions, and lessons that persist across sessions.
    """
    pass


@memory.command("add")
@click.argument("content")
@click.option(
    "--type", "-t", "mem_type",
    default="fact",
    type=click.Choice(["fact", "decision", "lesson", "preference", "context"]),
    help="Type of memory",
)
@click.option("--tag", "-g", multiple=True, help="Tags for this memory")
@click.option("--project", "-p", "project_path", default=".", help="Project path")
def memory_add(content: str, mem_type: str, tag: tuple, project_path: str):
    """Add a memory to the project store."""
    from pathlib import Path
    from conductor.memory import load_memory, save_memory

    project = Path(project_path).expanduser().resolve()
    store = load_memory(project)
    entry = store.add(content, mem_type, tags=list(tag))
    save_memory(store, project)

    click.echo(f"✅ Memory #{entry.id} added ({mem_type})")


@memory.command("search")
@click.argument("query")
@click.option("--project", "-p", "project_path", default=".", help="Project path")
def memory_search(query: str, project_path: str):
    """Search project memories."""
    from pathlib import Path
    from rich.console import Console
    from rich.table import Table
    from conductor.memory import load_memory, save_memory

    project = Path(project_path).expanduser().resolve()
    store = load_memory(project)
    results = store.search(query)
    save_memory(store, project)  # Save updated access counts

    if not results:
        click.echo(f"No memories matching '{query}'")
        return

    console = Console()
    table = Table(title=f"🔍 Memories matching '{query}'", border_style="cyan")
    table.add_column("ID", style="dim", width=4)
    table.add_column("Type", width=10)
    table.add_column("Content", ratio=1)
    table.add_column("Tags", style="dim", width=15)

    for entry in results:
        tags = ", ".join(entry.tags) if entry.tags else "—"
        table.add_row(str(entry.id), entry.type, entry.content, tags)

    console.print(table)


@memory.command("list")
@click.option("--type", "-t", "mem_type", default=None, help="Filter by type")
@click.option("--recent", "-r", "show_recent", is_flag=True, help="Show recent")
@click.option("--project", "-p", "project_path", default=".", help="Project path")
def memory_list(mem_type: str, show_recent: bool, project_path: str):
    """List all memories in the project store."""
    from pathlib import Path
    from rich.console import Console
    from rich.table import Table
    from conductor.memory import load_memory

    project = Path(project_path).expanduser().resolve()
    store = load_memory(project)

    if mem_type:
        entries = store.get_by_type(mem_type)
        title = f"📝 {mem_type.title()} Memories"
    elif show_recent:
        entries = store.get_recent(15)
        title = "⏰ Recent Memories"
    else:
        entries = store.entries
        title = f"📝 All Memories ({len(entries)} total)"

    if not entries:
        click.echo("No memories stored yet. Use 'conductor memory add' to create one.")
        return

    console = Console()
    table = Table(title=title, border_style="cyan")
    table.add_column("ID", style="dim", width=4)
    table.add_column("Type", width=10)
    table.add_column("Content", ratio=1)
    table.add_column("Tags", style="dim", width=15)
    table.add_column("Created", style="dim", width=12)

    for entry in entries:
        tags = ", ".join(entry.tags) if entry.tags else "—"
        created = entry.created[:10] if entry.created else "—"
        table.add_row(str(entry.id), entry.type, entry.content, tags, created)

    console.print(table)

    stats = store.stats()
    click.echo(f"\n  📊 {stats['total']} memories │ {stats['total_tags']} tags")


@memory.command("export")
@click.option("--project", "-p", "project_path", default=".", help="Project path")
def memory_export(project_path: str):
    """Export memories as markdown for agent context injection."""
    from pathlib import Path
    from conductor.memory import load_memory, export_memory_markdown

    project = Path(project_path).expanduser().resolve()
    store = load_memory(project)

    if not store.entries:
        click.echo("No memories to export.")
        return

    md = export_memory_markdown(store)
    click.echo(md)


@memory.command("extract")
@click.option("--project", "-p", "project_path", default=".", help="Project path")
def memory_extract(project_path: str):
    """Auto-extract memories from HANDOFF.md."""
    from pathlib import Path
    from conductor.memory import auto_extract_memories

    project = Path(project_path).expanduser().resolve()
    new_entries = auto_extract_memories(project)

    if not new_entries:
        click.echo("No new memories extracted (all already stored or none found).")
        return

    click.echo(f"✅ Extracted {len(new_entries)} new memories:")
    for entry in new_entries:
        click.echo(f"   #{entry.id} [{entry.type}] {entry.content[:60]}")


@main.command()
@click.argument("project_path", default=".")
def init(project_path: str):
    """Initialize Conductor in a project directory.

    Copies HANDOFF.md template and adds handoff protocol to the project.
    """
    import shutil
    from pathlib import Path

    project = Path(project_path).expanduser().resolve()
    templates_dir = Path(__file__).parent.parent.parent / "templates"

    if not project.exists():
        click.echo(f"Error: {project} does not exist.")
        return

    # Copy HANDOFF.md template
    handoff_dest = project / "HANDOFF.md"
    if handoff_dest.exists():
        click.echo(f"⚠️  HANDOFF.md already exists in {project.name}, skipping.")
    else:
        handoff_src = templates_dir / "HANDOFF.md.template"
        if handoff_src.exists():
            shutil.copy(handoff_src, handoff_dest)
            click.echo(f"✅ Created HANDOFF.md in {project.name}")
        else:
            # Create a basic one if template not found (e.g., pip install)
            handoff_dest.write_text(
                "# HANDOFF\n\n"
                "> Updated by AI agent at session end.\n\n"
                "## Latest Session\n\n"
                "No sessions recorded yet.\n"
            )
            click.echo(f"✅ Created HANDOFF.md in {project.name}")

    # Copy Error Book template
    error_dest = project / "docs" / "ERROR_BOOK.md"
    if not error_dest.parent.exists():
        error_dest.parent.mkdir(parents=True)
    if not error_dest.exists():
        error_src = templates_dir / "ERROR_BOOK.md.template"
        if error_src.exists():
            shutil.copy(error_src, error_dest)
        else:
            error_dest.write_text(
                "# AI Error Book\n\n> Track AI mistakes for trust calibration.\n"
            )
        click.echo(f"✅ Created docs/ERROR_BOOK.md in {project.name}")

    click.echo(f"\n🎵 Conductor initialized in {project.name}!")
    click.echo("   Next: Tell your AI agent to read HANDOFF.md at session start.")


if __name__ == "__main__":
    main()

