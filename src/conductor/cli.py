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
