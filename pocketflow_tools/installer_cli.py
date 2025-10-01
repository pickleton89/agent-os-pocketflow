"""Command-line interface for Agent OS + PocketFlow installation utilities.

This click-based CLI exposes the Python installer so that the framework
can be bootstrapped via ``uvx agent-os`` or an editable install.  The
entry point mirrors the eventual ``agent-os`` command defined in the
package metadata.
"""

from __future__ import annotations

import logging
from importlib import metadata
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from pocketflow_tools.installer import (
    AgentOsInstaller,
    InstallationOptions,
    InstallerError,
    InstallationReport,
)

console = Console()
DEFAULT_INSTALL_PATH = Path.home() / ".agent-os"

try:
    __version__ = metadata.version("agent-os-pocketflow")
except metadata.PackageNotFoundError:
    __version__ = "0.0.0"


def _configure_logging(verbose: bool) -> None:
    """Initialise logging for the installer run."""

    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")


def _render_report(report: InstallationReport, *, show_paths: bool) -> None:
    """Pretty-print the installation report to the console."""

    console.print(
        Panel.fit(
            f"Installation complete at [bold green]{report.install_path}[/bold green]",
            title="Agent OS + PocketFlow",
            border_style="green",
        )
    )

    summary_table = Table(box=None, show_header=False)
    summary_table.add_row("Created", str(len(report.created)))
    summary_table.add_row("Overwritten", str(len(report.overwritten)))
    console.print(summary_table)

    if report.warnings:
        warnings = "\n".join(f"• {message}" for message in report.warnings)
        console.print(Panel(warnings, title="Warnings", border_style="yellow"))

    if show_paths:
        if report.created:
            created_table = Table(title="Created Paths", box=None)
            created_table.add_column("Path")
            for item in sorted(report.created):
                created_table.add_row(str(item))
            console.print(created_table)
        if report.overwritten:
            overwritten_table = Table(title="Overwritten Paths", box=None)
            overwritten_table.add_column("Path")
            for item in sorted(report.overwritten):
                overwritten_table.add_row(str(item))
            console.print(overwritten_table)


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(version=__version__, prog_name="agent-os")
def cli() -> None:
    """Agent OS + PocketFlow installer commands."""


@cli.command()
@click.option(
    "install_path",
    "--install-path",
    type=click.Path(path_type=Path, file_okay=False, dir_okay=True),
    default=DEFAULT_INSTALL_PATH,
    show_default=str(DEFAULT_INSTALL_PATH),
    help="Destination directory for the base installation.",
)
@click.option(
    "include_pocketflow",
    "--pocketflow/--no-pocketflow",
    default=True,
    show_default=True,
    help="Include PocketFlow templates and toolkit resources.",
)
@click.option(
    "include_claude_code",
    "--claude-code/--no-claude-code",
    default=True,
    show_default=True,
    help="Include Claude Code integration assets.",
)
@click.option(
    "force",
    "--force/--no-force",
    default=False,
    show_default=True,
    help="Overwrite an existing installation at the target path.",
)
@click.option(
    "toolkit_source",
    "--toolkit-source",
    type=click.Path(path_type=Path, file_okay=False, dir_okay=True, exists=True),
    help="Override the packaged PocketFlow toolkit source directory.",
)
@click.option(
    "verbose",
    "--verbose/--quiet",
    default=False,
    help="Enable verbose logging output.",
)
@click.option(
    "show_paths",
    "--show-paths/--hide-paths",
    default=False,
    help="Display every created/overwritten path in the summary output.",
)
@click.option(
    "auto_confirm",
    "--yes/--prompt",
    default=False,
    help="Skip confirmation prompt and proceed immediately.",
)
def init(
    *,
    install_path: Path,
    include_pocketflow: bool,
    include_claude_code: bool,
    force: bool,
    toolkit_source: Optional[Path],
    verbose: bool,
    show_paths: bool,
    auto_confirm: bool,
) -> None:
    """Install the Agent OS + PocketFlow base resources."""

    _configure_logging(verbose)

    resolved_path = install_path.expanduser().resolve()
    resolved_toolkit = toolkit_source.expanduser().resolve() if toolkit_source else None

    if not auto_confirm:
        message = Panel.fit(
            "This will install Agent OS + PocketFlow resources to\n"
            f"[bold]{resolved_path}[/bold]. Continue?",
            border_style="cyan",
            title="Confirmation",
        )
        console.print(message)
        if not click.confirm("Proceed with installation?", default=True):
            console.print("Installation cancelled.")
            raise click.exceptions.Exit(0)

    installer = AgentOsInstaller(toolkit_source=resolved_toolkit)
    options = InstallationOptions(
        install_path=resolved_path,
        include_pocketflow=include_pocketflow,
        include_claude_code=include_claude_code,
        force=force,
    )

    try:
        report = installer.install_base(options)
    except InstallerError as exc:
        console.print(f"[bold red]Installation failed:[/bold red] {exc}")
        raise click.exceptions.Exit(1) from exc
    except Exception as exc:  # pragma: no cover - defensive catch
        console.print(f"[bold red]Unexpected error:[/bold red] {exc}")
        raise click.exceptions.Exit(1) from exc

    _render_report(report, show_paths=show_paths)


def main() -> None:
    """Entry point used by ``pyproject.toml`` scripts section."""

    cli(prog_name="agent-os")


if __name__ == "__main__":  # pragma: no cover - manual execution
    main()
