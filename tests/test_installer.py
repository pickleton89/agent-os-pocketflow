from pathlib import Path

import pytest

from pocketflow_tools.installer import (
    AgentOsInstaller,
    InstallationOptions,
    InstallationReport,
    InstallerError,
    ToolkitNotFoundError,
    install_base,
)
from pocketflow_tools.data import materialised_path


def test_install_base_creates_expected_structure(tmp_path):
    install_path = tmp_path / "agent-os"

    report = install_base(install_path)

    assert isinstance(report, InstallationReport)
    assert report.install_path == install_path.resolve()
    assert (install_path / "instructions").is_dir()
    assert (install_path / "standards").is_dir()
    assert (install_path / "shared").is_dir()
    assert (install_path / "templates").is_dir()
    assert (install_path / "claude-code").is_dir()
    assert (install_path / "setup" / "base.sh").is_file()
    assert (install_path / "setup.sh").is_file()
    assert (install_path / "config.yml").is_file()
    assert (install_path / "recaps").is_dir()
    commands = list((install_path / "commands").glob("*.md"))
    assert commands, "Expected at least one command markdown file"
    assert (install_path / "framework-tools").is_dir()
    assert not report.warnings


def test_install_base_requires_force_for_existing_path(tmp_path):
    install_path = tmp_path / "existing"
    install_path.mkdir()
    (install_path / "marker.txt").write_text("placeholder")

    with pytest.raises(InstallerError):
        install_base(install_path)

    report = install_base(install_path, force=True)
    assert install_path.resolve() == report.install_path
    assert "existing" in {p.name for p in report.created}


def test_install_base_skip_optional_components(tmp_path):
    install_path = tmp_path / "partial"

    options = InstallationOptions(
        install_path=install_path,
        include_pocketflow=False,
        include_claude_code=False,
        force=False,
    )
    report = AgentOsInstaller().install_base(options)

    assert not (install_path / "framework-tools").exists()
    assert not (install_path / "claude-code").exists()
    assert not (install_path / "templates").exists()
    assert (install_path / "instructions").exists()
    assert report.warnings == []


def test_install_toolkit_uses_custom_source(tmp_path):
    source = tmp_path / "toolkit-src"
    source.mkdir()
    (source / "sample.txt").write_text("custom toolkit")

    installer = AgentOsInstaller(toolkit_source=source)
    destination = tmp_path / "toolkit-dest"

    result = installer.install_toolkit(destination, force=True, atomic=False)

    assert destination.is_dir()
    assert (destination / "sample.txt").read_text() == "custom toolkit"
    assert result.source == source.resolve()
    assert destination in result.created


def test_install_toolkit_requires_force_when_destination_exists(tmp_path):
    source = tmp_path / "src"
    source.mkdir()
    (source / "file.txt").write_text("payload")

    destination = tmp_path / "dest"
    destination.mkdir()

    installer = AgentOsInstaller(toolkit_source=source)

    with pytest.raises(InstallerError):
        installer.install_toolkit(destination)


def test_install_toolkit_missing_source_raises(tmp_path):
    installer = AgentOsInstaller(toolkit_source=tmp_path / "missing")

    with pytest.raises(ToolkitNotFoundError):
        installer.install_toolkit(tmp_path / "dest", force=True)


def test_install_base_rejects_root_installation():
    root_path = Path(Path.cwd().anchor)

    with pytest.raises(InstallerError):
        install_base(root_path)


def test_install_base_warnings_capture_when_toolkit_absent(tmp_path, monkeypatch):
    install_path = tmp_path / "no-toolkit"

    def fake_toolkit_source(_self):
        from contextlib import contextmanager

        @contextmanager
        def _raise():
            raise ToolkitNotFoundError("PocketFlow toolkit could not be located")
            yield

        return _raise()

    monkeypatch.setattr(AgentOsInstaller, "_toolkit_source", fake_toolkit_source)
    installer = AgentOsInstaller()

    report = installer.install_base(InstallationOptions(install_path=install_path))

    assert any("PocketFlow toolkit could not be located" in warning for warning in report.warnings)
    assert not (install_path / "framework-tools").exists()


def test_materialised_path_provides_real_path():
    with materialised_path("instructions") as instructions_path:
        assert instructions_path.exists()
        assert instructions_path.is_dir()
        assert instructions_path.joinpath("core").exists()
