"""Agent OS + PocketFlow installer utilities.

This module replaces portions of the legacy shell-based installation
workflow with a Python implementation that can be executed from an
installed ``agent-os-pocketflow`` package.  It focuses on copying the
packaged resources (instructions, standards, templates, etc.) into a
target installation directory while providing safeguards around
overwriting existing installations and deploying the PocketFlow toolkit.
"""

from __future__ import annotations

import logging
import os
import shutil
import stat
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Iterator, List, Optional, Sequence, Union
from uuid import uuid4

from pocketflow_tools.data import materialised_path

PathLike = Union[str, os.PathLike[str]]


class InstallerError(RuntimeError):
    """Base error raised for installer issues."""


class ToolkitNotFoundError(InstallerError):
    """Raised when the PocketFlow toolkit source cannot be located."""


@dataclass
class InstallationOptions:
    """Parameters controlling a base installation operation."""

    install_path: Path
    include_pocketflow: bool = True
    include_claude_code: bool = True
    force: bool = False


@dataclass
class InstallationReport:
    """Summary of filesystem changes performed during installation."""

    install_path: Path
    created: List[Path] = field(default_factory=list)
    overwritten: List[Path] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def record_created(self, path: Path) -> None:
        self.created.append(path)

    def record_overwritten(self, path: Path) -> None:
        self.overwritten.append(path)

    def add_warning(self, message: str) -> None:
        self.warnings.append(message)


@dataclass
class ToolkitResult:
    """Summary of toolkit deployment."""

    source: Path
    destination: Path
    created: List[Path] = field(default_factory=list)
    overwritten: List[Path] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


class AgentOsInstaller:
    """High-level installer for Agent OS + PocketFlow resources."""

    def __init__(
        self,
        *,
        toolkit_source: Optional[PathLike] = None,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self.logger = logger or logging.getLogger(__name__)
        self.toolkit_source = (
            Path(toolkit_source).expanduser().resolve()
            if toolkit_source is not None
            else None
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def install_base(self, options: InstallationOptions) -> InstallationReport:
        """Install packaged resources into ``options.install_path``.

        Parameters
        ----------
        options:
            Structured installation parameters.
        """

        install_path = Path(options.install_path).expanduser().resolve()
        self._validate_install_path(install_path)

        report = InstallationReport(install_path=install_path)
        self.logger.debug("Installing Agent OS + PocketFlow to %s", install_path)

        if install_path.exists():
            if not options.force:
                raise InstallerError(
                    f"Install path {install_path} already exists. "
                    "Pass force=True to overwrite."
                )
            self.logger.debug("Removing existing installation at %s", install_path)
            self._remove_path(install_path, report)

        install_path.mkdir(parents=True, exist_ok=True)
        report.record_created(install_path)

        # Copy core resources
        instructions_dir = self._copy_resource_tree(
            ("instructions",), install_path / "instructions", report, force=options.force
        )
        self._copy_resource_tree(
            ("standards",), install_path / "standards", report, force=options.force
        )
        self._copy_resource_tree(
            ("shared",), install_path / "shared", report, force=options.force
        )

        if options.include_pocketflow:
            self._copy_resource_tree(
                ("templates",), install_path / "templates", report, force=options.force
            )

        if options.include_claude_code:
            self._copy_resource_tree(
                ("claude-code",),
                install_path / "claude-code",
                report,
                force=options.force,
            )

        self._copy_resource_tree(
            ("setup",), install_path / "setup", report, force=True, atomic=True
        )
        self._mark_shell_scripts(install_path / "setup")
        self._copy_resource_file(
            ("setup.sh",),
            install_path / "setup.sh",
            report,
            force=True,
            make_executable=True,
        )
        self._copy_resource_file(
            ("config.yml",), install_path / "config.yml", report, force=options.force
        )

        # Derived assets
        self._ensure_directory(install_path / "recaps", report)
        self._install_commands(instructions_dir, install_path / "commands", report)

        # Toolkit deployment (optional)
        if options.include_pocketflow:
            toolkit_destination = install_path / "framework-tools"
            try:
                toolkit_result = self.install_toolkit(
                    toolkit_destination,
                    force=True,
                    atomic=True,
                    report=report,
                )
                self.logger.debug(
                    "Installed toolkit from %s to %s",
                    toolkit_result.source,
                    toolkit_destination,
                )
            except ToolkitNotFoundError as exc:
                warning = str(exc)
                report.add_warning(warning)
                self.logger.debug("Toolkit installation skipped: %s", warning)

        return report

    def install_toolkit(
        self,
        destination: PathLike,
        *,
        force: bool = False,
        atomic: bool = True,
        report: Optional[InstallationReport] = None,
    ) -> ToolkitResult:
        """Copy the PocketFlow toolkit into ``destination``.

        Parameters
        ----------
        destination:
            Target directory for the toolkit copy.
        force:
            Remove the destination directory if it already exists.
        atomic:
            Copy into a temporary sibling directory and rename into place to
            avoid partial updates.
        report:
            Installation report to update alongside the toolkit-specific
            return value.
        """

        destination_path = Path(destination).expanduser().resolve()
        overwritten_paths: List[Path] = []

        if destination_path.exists():
            if not force:
                raise InstallerError(
                    f"Toolkit destination {destination_path} already exists. "
                    "Pass force=True to overwrite."
                )
            self._remove_path(destination_path, report)
            overwritten_paths.append(destination_path)

        with self._toolkit_source() as source:
            toolkit_report = ToolkitResult(
                source=source,
                destination=destination_path,
                overwritten=overwritten_paths.copy(),
            )

            copied_path = self._copy_tree(
                source,
                destination_path,
                report=report,
                atomic=atomic,
                force=False,
            )
            toolkit_report.created.append(copied_path)

        return toolkit_report

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @contextmanager
    def _toolkit_source(self) -> Iterator[Path]:
        if self.toolkit_source is not None:
            if not self.toolkit_source.exists():
                raise ToolkitNotFoundError(
                    f"Configured toolkit_source {self.toolkit_source} does not exist"
                )
            yield self.toolkit_source
            return

        try:
            with materialised_path("framework-tools") as packaged_toolkit:
                path = Path(packaged_toolkit)
                if path.exists():
                    yield path
                    return
        except FileNotFoundError:
            pass

        candidate = Path(__file__).resolve().parent.parent / "framework-tools"
        if candidate.exists():
            yield candidate
            return

        raise ToolkitNotFoundError(
            "PocketFlow toolkit could not be located. Provide toolkit_source "
            "when constructing AgentOsInstaller or ensure the repository "
            "includes a framework-tools directory."
        )

    def _validate_install_path(self, path: Path) -> None:
        anchor = Path(path.anchor)
        if path == anchor:
            raise InstallerError("Refusing to operate on filesystem root")
        if path == Path.home():
            raise InstallerError("Refusing to install directly into the home directory")

    def _remove_path(
        self, path: Path, report: Optional[InstallationReport] = None
    ) -> None:
        if not path.exists():
            return
        if path.is_dir() and not path.is_symlink():
            shutil.rmtree(path)
        else:
            path.unlink()
        if report is not None:
            report.record_overwritten(path)

    def _copy_resource_tree(
        self,
        relative_parts: Sequence[str],
        destination: Path,
        report: Optional[InstallationReport],
        *,
        force: bool,
        atomic: bool = False,
    ) -> Path:
        with materialised_path(*relative_parts) as source_path:
            return self._copy_tree(
                Path(source_path),
                destination,
                report=report,
                force=force,
                atomic=atomic,
            )

    def _copy_resource_file(
        self,
        relative_parts: Sequence[str],
        destination: Path,
        report: Optional[InstallationReport],
        *,
        force: bool,
        make_executable: bool = False,
    ) -> Path:
        with materialised_path(*relative_parts) as source_path:
            copied = self._copy_file(
                Path(source_path), destination, report=report, force=force
            )
        if make_executable:
            self._mark_executable(copied)
        return copied

    def _copy_tree(
        self,
        source: Path,
        destination: Path,
        *,
        report: Optional[InstallationReport],
        force: bool,
        atomic: bool,
    ) -> Path:
        if destination.exists():
            if not force:
                raise InstallerError(
                    f"Destination {destination} already exists. Pass force=True to overwrite."
                )
            self._remove_path(destination, report)

        destination.parent.mkdir(parents=True, exist_ok=True)

        if atomic:
            temp_destination = destination.parent / f".{destination.name}.tmp-{uuid4().hex}"
            shutil.copytree(source, temp_destination)
            os.replace(temp_destination, destination)
        else:
            shutil.copytree(source, destination)

        if report is not None:
            report.record_created(destination)
        return destination

    def _copy_file(
        self,
        source: Path,
        destination: Path,
        *,
        report: Optional[InstallationReport],
        force: bool,
    ) -> Path:
        if destination.exists():
            if not force:
                raise InstallerError(
                    f"Destination file {destination} already exists. Pass force=True to overwrite."
                )
            self._remove_path(destination, report)

        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        if report is not None:
            report.record_created(destination)
        return destination

    def _ensure_directory(
        self, path: Path, report: Optional[InstallationReport]
    ) -> None:
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            if report is not None:
                report.record_created(path)

    def _install_commands(
        self, instructions_path: Path, commands_path: Path, report: InstallationReport
    ) -> None:
        self._ensure_directory(commands_path, report)

        if not instructions_path.exists():
            report.add_warning(
                f"Instructions directory {instructions_path} not found; skipping command copies"
            )
            return

        seen: set[str] = set()
        candidate_dirs: Iterable[Path] = (
            instructions_path / "core",
            instructions_path,
        )
        for directory in candidate_dirs:
            if not directory.is_dir():
                continue
            for source_file in sorted(directory.glob("*.md")):
                target = commands_path / source_file.name
                if target.name in seen:
                    continue
                shutil.copy2(source_file, target)
                report.record_created(target)
                seen.add(target.name)

    def _mark_shell_scripts(self, directory: Path) -> None:
        if not directory.exists():
            return
        for script in directory.rglob("*.sh"):
            self._mark_executable(script)

    def _mark_executable(self, path: Path) -> None:
        try:
            mode = path.stat().st_mode
            path.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        except OSError:
            # Non-fatal: on some platforms (e.g., Windows) chmod may fail.
            pass


def install_base(
    install_path: PathLike,
    *,
    include_pocketflow: bool = True,
    include_claude_code: bool = True,
    force: bool = False,
    toolkit_source: Optional[PathLike] = None,
    logger: Optional[logging.Logger] = None,
) -> InstallationReport:
    """Convenience wrapper around :class:`AgentOsInstaller`.

    This provides a functional-style API that mirrors the eventual CLI
    surface while remaining easy to import within tests.
    """

    installer = AgentOsInstaller(toolkit_source=toolkit_source, logger=logger)
    options = InstallationOptions(
        install_path=Path(install_path),
        include_pocketflow=include_pocketflow,
        include_claude_code=include_claude_code,
        force=force,
    )
    return installer.install_base(options)


__all__ = [
    "AgentOsInstaller",
    "InstallationOptions",
    "InstallationReport",
    "InstallerError",
    "ToolkitNotFoundError",
    "ToolkitResult",
    "install_base",
]
