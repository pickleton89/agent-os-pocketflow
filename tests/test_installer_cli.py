from __future__ import annotations

from pathlib import Path

from click.testing import CliRunner

from pocketflow_tools.installer_cli import cli


def test_cli_rejects_root_install_path():
    runner = CliRunner()
    root_path = Path(Path.cwd().anchor)

    result = runner.invoke(
        cli,
        [
            "init",
            "--install-path",
            str(root_path),
            "--yes",
        ],
    )

    assert result.exit_code == 1
    assert "Refusing to operate on filesystem root" in result.output


def test_cli_rejects_unknown_toolkit_source(tmp_path):
    runner = CliRunner()
    install_path = tmp_path / "install"
    invalid_toolkit = tmp_path / "missing"

    result = runner.invoke(
        cli,
        [
            "init",
            "--install-path",
            str(install_path),
            "--toolkit-source",
            str(invalid_toolkit),
            "--yes",
        ],
    )

    assert result.exit_code != 0
    assert "does not exist" in result.output


def test_cli_requires_force_when_install_exists(tmp_path):
    runner = CliRunner()
    install_path = tmp_path / "existing"
    install_path.mkdir()
    (install_path / "framework-tools").mkdir()

    result = runner.invoke(
        cli,
        [
            "init",
            "--install-path",
            str(install_path),
            "--yes",
        ],
    )

    assert result.exit_code == 1
    assert "already exists" in result.output
